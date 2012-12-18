from __future__ import unicode_literals
from stat_file_source.common.state import State
from stat_file_source.handler.handler import Handler

class SingleKeyHandler(Handler):

    # spec: str, (str, State -> bool), (str, State -> str), object -> SingleKeyHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer, value):
        self._key_value_delimiter = key_value_delimiter
        self._known_key_predicate = known_key_predicate
        self._key_transformer = key_transformer
        self._value = value

    # spec: str, [str], (str, State -> str), object -> SingleKeyHandler
    @classmethod
    def create_with_known_key_list(cls, key_value_delimiter, known_key_list, key_transformer, value):
        known_key_predicate = lambda key, state: key in known_key_list
        return cls(key_value_delimiter, known_key_predicate, key_transformer, value)

    # spec: str, (str, State -> bool), (str, State -> str), object -> SingleKeyHandler
    @classmethod
    def create_with_known_key_predicate(cls, key_value_delimiter, known_key_predicate, key_transformer, value):
        return cls(key_value_delimiter, known_key_predicate, key_transformer, value)

    # spec: str, State -> (bool, State)
    def process(self, source, state):
        if not self._key_value_delimiter in source:
            key = source
            if self._known_key_predicate(key, state):
                final_key = self._key_transformer(key, state)
                new_items = dict(state.items)
                new_items[final_key] = self._value
                return (True, State(state.state_id, state.state_data, new_items))
            return (False, state)
        return (False, state)

__author__ = 'andrey.ushakov'
