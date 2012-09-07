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
