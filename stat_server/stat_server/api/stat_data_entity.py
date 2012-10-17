from __future__ import unicode_literals

class StatDataEntity(object):

    def __init__(self, source = None, category = None, timemarker = None, data = None, id = None):
        self._id = id
        self._source = source
        self._category = category
        self._timemarker = timemarker
        self._data = data

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def timemarker(self):
        return self._timemarker

    @timemarker.setter
    def timemarker(self, value):
        self._timemarker = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    # probably unnecessary attribute
    _id = None
    _source = None
    _category = None
    _timemarker = None
    _data = None

__author__ = 'andrey.ushakov'
