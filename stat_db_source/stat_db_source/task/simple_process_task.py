from __future__ import unicode_literals
from stat_source_common.entity import data_item
from stat_db_source.task.process_task import ProcessTask

class SimpleProcessTask(ProcessTask):

    # spec: [[(str, str)]] -> [DataItem]
    def process(self, intermediate_data):
        dest = []
        for row in intermediate_data:
            dest.extend([data_item.DataItem(item[0], item[1]) for item in row])
        return dest

__author__ = 'andrey.ushakov'
