from __future__ import unicode_literals

class DictHelper(object):

    @staticmethod
    def get_or_create(dict, key, default_value):
        if key not in dict:
            dict[key] = default_value
        return dict[key]

__author__ = 'andrey.ushakov'
