from __future__ import unicode_literals

class StatDataItem(object):

    # spec: int, str, str, datetime, str -> StatDataItem
    def __init__(self, id, source, category, timemarker, data):
        self._id = id
        self._source = source
        self._category = category
        self._timemarker = timemarker
        self._data = data

    # spec: None -> int
    @property
    def id(self):
        return self._id

    # spec: None -> str
    @property
    def source(self):
        return self._source

    # spec: None -> str
    @property
    def category(self):
        return self._category

    # spec: None -> datetime
    @property
    def timemarker(self):
        return self._timemarker

    # spec: None -> str
    @property
    def data(self):
        return self._data

    # spec: StatData -> bool
    def __eq__(self, other):
        if not other.__class__ == StatDataItem:
            return False
        return self._id == other._id and\
               self._source == other._source and\
               self._category == other._category and\
               self._timemarker == other._timemarker and\
               self._data == other._data

    # spec: None -> int
    def __hash__(self):
        result = hash(self._id)
        result = (result * 13) ^ hash(self._source)
        result = (result * 13) ^ hash(self._category)
        result = (result * 13) ^ hash(self._timemarker)
        result = (result * 13) ^ hash(self._data)
        return result

class StatData(object):

    # spec: (int, int), [StatDataItem] -> StatData
    def __init__(self, id_range, stat_data_items):
        self._id_range = id_range
        self._stat_data_items = stat_data_items

    # spec: None -> (int, int)
    @property
    def id_range(self):
        return self._id_range

    # spec: None -> [StatDataItem]
    @property
    def stat_data_items(self):
        return self._stat_data_items

__author__ = 'andrey.ushakov'
