from __future__ import unicode_literals
from src.handler.base_key_value_handler import BaseKeyValueHandler

class TransformKeyValueHandler(BaseKeyValueHandler):

    # spec: str, [str], (str, State -> str), (str -> object) -> TransformKeyValueHandler
    def __init__(self, key_value_delimiter, known_keys, key_transformer, transform_fun):
        BaseKeyValueHandler.__init__(self, key_value_delimiter, known_keys, key_transformer, [])
        self._transform_fun = transform_fun

    # spec: [object], str -> [object]
    def _define_value(self, old_value, item_value):
        new_value = list(old_value)
        new_value.append(self._transform_fun(item_value))
        return new_value

    _transform_fun =None


__author__ = 'andrey.ushakov'
