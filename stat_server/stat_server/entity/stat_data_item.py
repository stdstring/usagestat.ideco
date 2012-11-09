from __future__ import unicode_literals

class StatDataItem(object):

    # spec: str, str, datetime, str -> StatDataItem
    def __init__(self, source=None, category=None, timemarker=None, data=None):
        self._source = source
        self._category = category
        self._timemarker = timemarker
        self._data = data

    # spec: None -> str
    @property
    def source(self):
        return self._source

    # spec: str -> None
    @source.setter
    def source(self, value):
        self._source = value

    # spec: None -> str
    @property
    def category(self):
        return self._category

    # spec: str -> None
    @category.setter
    def category(self, value):
        self._category = value

    # spec: None -> datetime
    @property
    def timemarker(self):
        return self._timemarker

    # spec: datetime -> None
    @timemarker.setter
    def timemarker(self, value):
        self._timemarker = value

    # spec: None -> str
    @property
    def data(self):
        return self._data

    # spec: str -> None
    @data.setter
    def data(self, value):
        self._data = value

__author__ = 'andrey.ushakov'
