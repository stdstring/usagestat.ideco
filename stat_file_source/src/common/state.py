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

    _state_id = None
    _state_data = None
    _items = {}

__author__ = 'andrey.ushakov'