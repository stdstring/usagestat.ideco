from __future__ import unicode_literals
from stat_file_source.handler.handler import Handler
from stat_file_source.handler.transform_key_value_handler import TransformKeyValueHandler
from stat_file_source.handler.single_key_handler import SingleKeyHandler

class TransformVariableHandler(Handler):

    # spec:
    # key_value_delimiter: str
    # known_key_predicate: str, State -> bool
    # key_transformer: str, str, State -> str
    # transform_fun: str -> object
    # value: object
    # rt: TransformVariableHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer, transform_fun, value):
        self._key_value_handler = TransformKeyValueHandler(key_value_delimiter, known_key_predicate, key_transformer, transform_fun)
        self._single_key_handler = SingleKeyHandler.create_with_known_key_predicate(key_value_delimiter, known_key_predicate, key_transformer, value)

    # spec:
    # key_value_delimiter: str
    # known_key_list: [str]
    # key_transformer: str, str, State -> str
    # transform_fun: str -> object
    # value: object
    # rt: TransformVariableHandler
    @classmethod
    def create_with_known_key_list(cls, key_value_delimiter, known_key_list, key_transformer, transform_fun, value):
        known_key_predicate = lambda key, state: key in known_key_list
        return cls(key_value_delimiter, known_key_predicate, key_transformer, transform_fun, value)

    # spec:
    # key_value_delimiter: str
    # known_key_predicate: str, State -> bool
    # key_transformer: str, str, State -> str
    # transform_fun: str -> object
    # value: object
    # rt: TransformVariableHandler
    @classmethod
    def create_with_known_key_predicate(cls, key_value_delimiter, known_key_predicate, key_transformer, transform_fun, value):
        return cls(key_value_delimiter, known_key_predicate, key_transformer, transform_fun, value)

    # spec: str, State -> (bool, State)
    def process(self, source, state):
        (result, state) = self._key_value_handler.process(source, state)
        if result:
            return (True, state)
        return self._single_key_handler.process(source, state)

__author__ = 'andrey.ushakov'
