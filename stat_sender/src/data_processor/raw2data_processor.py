from __future__ import unicode_literals
import sys
from src.common.stat_data import StatDataItem, StatData
from data_processor import DataProcessor

class Raw2DataProcessor(DataProcessor):

    # spec : (int, str, datetime, str) -> StatData
    def process(self, raw_data):
        stat_data_items = []
        min_id = sys.maxint
        max_id = 0
        for raw_data_item in raw_data:
            stat_data_item = StatDataItem(raw_data_item[0], raw_data_item[1], raw_data_item[2], raw_data_item[3])
            stat_data_items.append(stat_data_item)
            if min_id > stat_data_item.id:
                min_id = stat_data_item.id
            if max_id < stat_data_item.id:
                max_id = stat_data_item.id
        return StatData((min_id, max_id), stat_data_items)

__author__ = 'andrey.ushakov'
