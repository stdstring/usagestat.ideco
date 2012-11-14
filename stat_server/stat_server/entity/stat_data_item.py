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

    # spec: None -> str
    def __str__(self):
        format_str = 'StatDataItem(source="{source:s}", category="{category:s}", timemarker="{timemarker:%Y-%m-%d %H:%M:%S}", data="{data:s}")'
        return format_str.format(source=self.source, category=self.category, timemarker=self.timemarker, data=self.data)

    # spec: None -> str
    def __repr__(self):
        return self.__str__()

    # spec: StatDataItem -> bool
    def __eq__(self, other):
        if not other.__class__ == StatDataItem:
            return False
        return self._source == other._source and\
               self._category == other._category and\
               self._timemarker == other._timemarker and\
               self._data == other._data

    # spec: None -> int
    def __hash__(self):
        result = hash(self._source)
        result = (result * 13) ^ hash(self._source)
        result = (result * 13) ^ hash(self._category)
        result = (result * 13) ^ hash(self._timemarker)
        result = (result * 13) ^ hash(self._data)
        return result

__author__ = 'andrey.ushakov'
