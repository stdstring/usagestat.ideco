from __future__ import unicode_literals
from stat_source_common.entity import data_item

class FileSourceCollectTaskImpl(object):

    # spec: str, FileSourceCollector, callable, Storage, Logger -> FileSourceCollectTask
    def __init__(self, source_id, collector, source_provider, storage, logger):
        self._source_id = source_id
        self._collector = collector
        self._source_provider = source_provider
        self._storage = storage
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        self._logger.info('execute() enter')
        try:
            source_data = self._read_file_content()
            dest_data = self._collector.collect(source_data)
            self._write_data(dest_data)
        except Exception:
            self._logger.exception('exception in execute()')
            return False
        self._logger.info('execute() exit')
        return True

    # spec: None -> [str]
    def _read_file_content(self):
        self._logger.info('_read_file_content() enter')
        try:
            data = self._source_provider()
            self._logger.info('_read_file_content() exit')
            return data
        except Exception:
            self._logger.exception('exception in _read_file_content()')
            raise

    # spec: {str: object | [object]} -> None
    def _write_data(self, data_dict):
        self._logger.info('_write_data(data_dict) enter')
        data_list = self._prepare_data(data_dict)
        self._storage.save_data(self._source_id, data_list)
        self._logger.info('_write_data(data_dict) exit')

    # spec: {str: object | [object]} -> [(str, object)]
    def _prepare_data(self, data_dict):
        dest_data = []
        for category in data_dict:
            value = data_dict[category]
            if isinstance(value, list):
                for item in value:
                    dest_data.append(data_item.DataItem(category, item))
            else:
                dest_data.append(data_item.DataItem(category, value))
        return dest_data

__author__ = 'andrey.ushakov'
