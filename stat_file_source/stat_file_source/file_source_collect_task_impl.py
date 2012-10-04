from __future__ import unicode_literals
import logging
from stat_file_source.common.logger_helper import LoggerHelper

class FileSourceCollectTaskImpl(object):

    # spec: str, FileSourceCollector, str, Storage, Logger -> FileSourceCollectTask
    def __init__(self, source_id, collector, source_filename, storage, logger = logging.getLogger('stat_file_source.file_source_collect_task')):
        self._source_id = source_id
        self._collector = collector
        self._source_filename = source_filename
        self._storage = storage
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        self._logger.info('execute() enter')
        try:
            source_data = self._read_file_content()
            dest_data = self._collector.collect(source_data)
            write_result = self._write_data(dest_data)
            str_write_result = LoggerHelper.bool_result_to_str(write_result)
            self._logger.info('execute() exit with result %(result)s' % {'result': str_write_result})
            return write_result
        except Exception:
            self._logger.exception('exception in FileSourceCollectTask.execute()')
            return False

    # spec: None -> [str]
    def _read_file_content(self):
        self._logger.info('_read_file_content() enter')
        source = open(self._source_filename, 'r')
        try:
            data = source.readlines()
            self._logger.info('_read_file_content() exit')
            return data
        except Exception:
            self._logger.exception('exception in _read_file_content()')
            raise
        finally:
            source.close()

    # spec: {str: object | [object]} -> bool
    def _write_data(self, data_dict):
        self._logger.info('_write_data(data_dict) enter')
        #storage = SqliteStorageImpl(self._db_dest_filename, self._logger.getChild('sqlite_storage_impl'))
        data_list = self._prepare_data(data_dict)
        result = self._storage.save_data(self._source_id, data_list)
        str_result = LoggerHelper.bool_result_to_str(result)
        self._logger.info('_write_data(data_dict) exit with result %(result)s' % {'result': str_result})
        return result

    # spec: {str: object | [object]} -> [(str, object)]
    def _prepare_data(self, data_dict):
        dest_data = []
        for category in data_dict:
            value = data_dict[category]
            if isinstance(value, list):
                for item in value:
                    dest_data.append((category, item))
            else:
                dest_data.append((category, value))
        return dest_data

    _source_id = None
    _collector = None
    _source_filename = None
    _storage = None
    _logger = None

__author__ = 'andrey.ushakov'
