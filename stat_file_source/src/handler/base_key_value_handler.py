from __future__ import unicode_literals
from src.common.dict_helper import DictHelper
from src.common.state import State
from src.handler.handler import Handler

class BaseKeyValueHandler(Handler):

    # spec: str, [str], (str, State -> str) -> BaseKeyValueHandler
    def __init__(self, key_value_delimiter, known_keys, key_transformer):
        self._key_value_delimiter = key_value_delimiter
        self._known_keys = known_keys
        self._key_transformer = key_transformer

    # spec: str, State -> (bool, State)
    def process(self, source, state):
        delimiter_position = self._get_delimiter_position(source)
        if delimiter_position > -1:
            key = source[0:delimiter_position]
            value = source[delimiter_position + len(self._key_value_delimiter): len(source) - delimiter_position - len(self._key_value_delimiter)]
            if key in self._known_keys:
                final_key = self._key_transformer(key, state)
                items = DictHelper.get_or_create(state, final_key, [])
                items[final_key] = self._define_value(items[key], value)
                return (True, State(state.state_id, items))
            else:
                return (False, state)
        else:
            return (False, state)

    # spec: str -> int
    def _get_delimiter_position(self, source):
        return source.find(self._key_value_delimiter)

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        raise NotImplementedError()

    _key_value_delimiter = None
    _known_keys = []
    _key_transformer = None

__author__ = 'andrey.ushakov'
