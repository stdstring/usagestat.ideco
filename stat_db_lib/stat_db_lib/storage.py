from __future__ import unicode_literals

class Storage(object):

    # spec: str, [(str, str)] -> bool
    def save_data(self, source_id, data_list):
        raise NotImplementedError()

    # spec: str, str, str -> bool
    def save_item(self, source_id, category, data):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
