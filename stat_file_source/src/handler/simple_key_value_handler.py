from __future__ import unicode_literals
from src.handler.base_key_value_handler import BaseKeyValueHandler

class SimpleKeyValueHandler(BaseKeyValueHandler):

    def __init__(self, key_value_delimiter, known_keys):
        BaseKeyValueHandler.__init__(self, key_value_delimiter, known_keys)

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        return old_value.append(item_value)

__author__ = 'andrey.ushakov'
