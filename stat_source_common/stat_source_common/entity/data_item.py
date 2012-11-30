from __future__ import unicode_literals
from collections import namedtuple

class DataItem(namedtuple('DataItem', ['category', 'data'])):

    def __init__(self, category, data):
        super(DataItem, self).__init__(category, data)

    def __str__(self):
        if isinstance(self.category, basestring):
            str_category = "'{0}'".format(self.category)
        else:
            str_category = self.category
        if isinstance(self.data, basestring):
            str_data = "'{0}'".format(self.data)
        else:
            str_data = self.data
        return 'DataItem(category={category!s}, data={data!s})'.format(category=str_category, data=str_data)

    def __repr__(self):
        return self.__str__()

__author__ = 'andrey.ushakov'
