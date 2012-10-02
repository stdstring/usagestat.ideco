from __future__ import unicode_literals

class State(object):

    # spec: str, str, [object] -> State
    def __init__(self, state_id, state_data, items):
        self._state_id = state_id
        self._state_data = state_data
        self._items = items

    # spec: None -> str
    @property
    def state_id(self):
        return self._state_id

    # spec: None -> str
    @property
    def state_data(self):
        return self._state_data

    # spec: None -> {str: [object]}
    @property
    def items(self):
        return self._items

    def __eq__(self, other):
        if not isinstance(other, State):
            raise TypeError()
        return self._state_id == other._state_id and\
               self._state_data == other._state_data and\
               self._items == other._items
        pass

    def __hash__(self):
        result = hash(self._state_id)
        result = (result * 13) ^ hash(self._state_data)
        result = (result * 13) ^ hash(self._items)
        return result

    _state_id = None
    _state_data = None
    _items = {}

__author__ = 'andrey.ushakov'