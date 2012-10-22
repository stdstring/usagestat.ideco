from __future__ import unicode_literals
from datetime import datetime

class StatDataEntity(object):

    # spec: str, str, datetime, str, int -> StatDataEntity
    def __init__(self, source = None, category = None, timemarker = None, data = None, id = None):
        # probably unnecessary attribute
        self._id = id
        self._source = source
        self._category = category
        self._timemarker = timemarker
        self._data = data

    # spec: None -> int
    @property
    def id(self):
        return self._id

    # spec: int -> None
    @id.setter
    def id(self, value):
        self._id = value

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

    # spec: (str | datetime) -> None
    @timemarker.setter
    def timemarker(self, value):
        if isinstance(value, basestring):
            self._timemarker = self._str_2_time(value)
        else:
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
        storage = []
        # id
        if self._id is not None:
            storage.append('id = {0:d}'.format(self._id))
        else:
            storage.append('id = None')
        # source
        if self._source is not None:
            storage.append('source = {0:s}'.format(self._source))
        else:
            storage.append('source = None')
        # category
        if self._category is not None:
            storage.append('category = {0:s}'.format(self._category))
        else:
            storage.append('category = None')
        # timemarker
        if self._timemarker is not None:
            storage.append('timemarker = {0:%Y-%m-%d %H:%M:%S}'.format(self._timemarker))
        else:
            storage.append('timemarker = None')
        # data
        if self._data is not None:
            storage.append('data = {0:s}'.format(self._data))
        else:
            storage.append('data = None')
        return 'StatDataEntity: ' + ','.join(storage)

    # spec: str -> datetime
    def _str_2_time(self, source_str):
        return datetime.strptime(source_str, '%Y-%m-%d %H:%M:%S')

__author__ = 'andrey.ushakov'
