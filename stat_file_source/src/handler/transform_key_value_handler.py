from __future__ import unicode_literals
from src.handler.base_key_value_handler import BaseKeyValueHandler

class TransformKeyValueHandler(BaseKeyValueHandler):

    def __init__(self, key_value_delimiter, known_keys, transform_fun):
        BaseKeyValueHandler.__init__(self, key_value_delimiter, known_keys)
        self._transform_fun = transform_fun

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        return old_value.append(self._transform_fun(item_value))

    _transform_fun =None


__author__ = 'andrey.ushakov'