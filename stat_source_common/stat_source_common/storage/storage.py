from __future__ import unicode_literals

class Storage(object):

    # spec: str, [DataItem] -> bool
    def save_data(self, source_id, data_item_list):
        raise NotImplementedError()

    # spec: str, DataItem -> bool
    def save_item(self, source_id, data_item):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
