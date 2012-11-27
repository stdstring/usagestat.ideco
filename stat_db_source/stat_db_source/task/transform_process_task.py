from __future__ import unicode_literals
from stat_source_common.entity import data_item
from stat_db_source.task.process_task import ProcessTask

class TransformProcessTask(ProcessTask):

    # spec:
    def __init__(self, category_transformer, data_transformer):
        self._category_transformer = category_transformer
        self._data_transformer = data_transformer

    # spec: [[(...)]] -> [DataItem]
    def process(self, intermediate_data):
        dest = []
        for row in intermediate_data:
            dest.extend([data_item.DataItem(self._category_transformer(item), self._data_transformer(item)) for item in row])
        return dest

__author__ = 'andrey.ushakov'
