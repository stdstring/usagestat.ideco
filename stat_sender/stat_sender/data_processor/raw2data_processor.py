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
        for raw_data_item in raw_data:
            timemarker = self._str_2_datetime(raw_data_item[3])
            stat_data_item = StatDataItem(raw_data_item[0], raw_data_item[1], raw_data_item[2], timemarker, raw_data_item[4])
            stat_data_items.append(stat_data_item)
            if min_id > stat_data_item.id:
                min_id = stat_data_item.id
            if max_id < stat_data_item.id:
                max_id = stat_data_item.id
        return StatData((min_id, max_id), stat_data_items)

    # spec: str -> datetime
    def _str_2_datetime(self, source):
        return datetime.strptime(source, '%Y-%m-%d %H:%M:%S')

__author__ = 'andrey.ushakov'
