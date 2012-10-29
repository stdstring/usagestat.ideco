from __future__ import unicode_literals
from datetime import datetime
import sys
from stat_sender.common.stat_data import StatDataItem, StatData
from data_processor import DataProcessor

class Raw2DataProcessor(DataProcessor):

    # spec : [(int, str, str, str, str)] -> StatData
    def process(self, raw_data):
        stat_data_items = []
        min_id = sys.maxint
        max_id = 0
        for (id, source, category, str_timemarker, data) in raw_data:
            timemarker = datetime.strptime(str_timemarker, '%Y-%m-%d %H:%M:%S')
            stat_data_item = StatDataItem(id, source, category, timemarker, data)
            stat_data_items.append(stat_data_item)
            if min_id > stat_data_item.id:
                min_id = stat_data_item.id
            if max_id < stat_data_item.id:
                max_id = stat_data_item.id
        return StatData((min_id, max_id), stat_data_items)

__author__ = 'andrey.ushakov'
