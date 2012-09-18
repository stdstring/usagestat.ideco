from __future__ import unicode_literals

class StatDataItem(object):

    def __init__(self, id, category, timemarker, data):
        self._id = id
        self._category = category
        self._timemarker = timemarker
        self._data = data

    # spec: None -> int
    @property
    def id(self):
        return self._id

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
            raise TypeError
        return self._id == other._id and\
               self._category == other._category and \
               self._timemarker == other._timemarker  and\
               self._data == other._data

    # spec: None -> int
    def __hash__(self):
        result = hash(self._id)
        result = (result * 13) ^ hash(self._category)
        result = (result * 13) ^ hash(self._timemarker)
        result = (result * 13) ^ hash(self._data)
        return result

    _id = None
    _category = None
    _timemarker = None
    _data = None

class StatData(object):

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

    _id_range = None
    _stat_data_items = []

__author__ = 'andrey.ushakov'
