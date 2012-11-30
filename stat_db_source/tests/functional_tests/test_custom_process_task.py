from __future__ import unicode_literals
from stat_source_common.entity import data_item
from stat_db_source.task.process_task import ProcessTask

class TestCustomProcessTask(ProcessTask):

    # spec: [[(...)]] -> [DataItem]
    def process(self, intermediate_data):
        # intermediate_data = [[rows from main_data_storage], [rows from user_data_storage]]
        # rows from main_data_storage = (str(uuid), str, str, str)
        # rows from user_data_storage = (str(uuid), str)
        dest = []
        main_data_storage = intermediate_data[0]
        user_data_storage = intermediate_data[1]
        for main_data_row in main_data_storage:
            user_id = main_data_row[0]
            user_data_subset = filter(lambda row: row[0] == user_id, user_data_storage)
            if len(user_data_subset) == 1:
                user_data = user_data_subset[0][1]
                category = 'users_cat.{user_data:s}.{category:s}'.format(user_data=user_data, category=main_data_row[1])
                data = self._data_transformer(main_data_row[2], main_data_row[3])
                dest.append(data_item.DataItem(category, data))
        return dest

    # spec:
    def _data_transformer(self, data1, data2):
        if data1 is not None:
            return '-{0:s}-'.format(data1)
        if data2 is not None:
            return '-{0:s}-'.format(data2)
        return '-empty-'

__author__ = 'andrey.ushakov'
