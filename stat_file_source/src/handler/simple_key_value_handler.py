from __future__ import unicode_literals
from src.handler.base_key_value_handler import BaseKeyValueHandler

class SimpleKeyValueHandler(BaseKeyValueHandler):

    # spec: str, [str], (str, State -> str) -> SimpleKeyValueHandler
    def __init__(self, key_value_delimiter, known_keys, key_transformer):
        BaseKeyValueHandler.__init__(self, key_value_delimiter, known_keys, key_transformer, [])

    # spec: [str], str -> [str]
    def _define_value(self, old_value, item_value):
        new_value = list(old_value)
        new_value.append(item_value)
        return new_value

__author__ = 'andrey.ushakov'
