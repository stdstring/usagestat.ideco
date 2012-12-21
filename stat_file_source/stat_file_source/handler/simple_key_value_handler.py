from __future__ import unicode_literals
from stat_file_source.handler.base_key_value_handler import BaseKeyValueHandler

class SimpleKeyValueHandler(BaseKeyValueHandler):

    # spec:
    # key_value_delimiter: str
    # known_key_predicate: str, State -> bool
    # key_transformer: str, str, State -> str
    # rt: SimpleKeyValueHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer):
        super(SimpleKeyValueHandler, self).__init__(key_value_delimiter, known_key_predicate, key_transformer, None)

    # spec:
    # key_value_delimiter: str
    # known_key_list: [str]
    # key_transformer: str, str, State -> str
    # rt: SimpleKeyValueHandler
    @classmethod
    def create_with_known_key_list(cls, key_value_delimiter, known_key_list, key_transformer):
        return cls(key_value_delimiter, lambda key, state: key in known_key_list, key_transformer)

    # spec:
    # key_value_delimiter: str
    # known_key_predicate: str, State -> bool
    # key_transformer: str, str, State -> str
    # rt: SimpleKeyValueHandler
    @classmethod
    def create_with_known_key_predicate(cls, key_value_delimiter, known_key_predicate, key_transformer):
        return cls(key_value_delimiter, known_key_predicate, key_transformer)

    # spec: str, str -> str
    def _define_value(self, old_value, item_value):
        return item_value

__author__ = 'andrey.ushakov'
