from __future__ import unicode_literals

class Storage(object):

    # spec: [(str, str)] -> bool
    def save_data(self, data_list):
        raise NotImplementedError()

    # spec: str, str -> bool
    def save_item(self, category, data):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
