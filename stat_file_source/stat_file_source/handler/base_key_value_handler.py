from __future__ import unicode_literals
from stat_file_source.common.state import State
from stat_file_source.handler.handler import Handler

class BaseKeyValueHandler(Handler):

    # spec: str, (str, State -> bool), (str, State -> str), object -> BaseKeyValueHandler
    def __init__(self, key_value_delimiter, known_key_predicate, key_transformer, item_init_value):
        self._key_value_delimiter = key_value_delimiter
        self._known_key_predicate = known_key_predicate
        self._key_transformer = key_transformer
        self._item_init_value = item_init_value

    # spec: str, State -> (bool, State)
    def process(self, source, state):
        delimiter_position = self._get_delimiter_position(source)
        if delimiter_position > -1:
            key = source[0: delimiter_position]
            value = source[delimiter_position + len(self._key_value_delimiter): len(source)]
            if self._known_key_predicate(key, state):
                final_key = self._key_transformer(key, state)
                new_items = dict(state.items)
                key_values = new_items.setdefault(final_key, self._item_init_value)
                new_items[final_key] = self._define_value(key_values, value)
                return (True, State(state.state_id, state.state_data, new_items))
            return (False, state)
        return (False, state)

    # spec: str -> int
    def _get_delimiter_position(self, source):
        return source.find(self._key_value_delimiter)

    # spec: object, str -> object
    def _define_value(self, old_value, item_value):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
