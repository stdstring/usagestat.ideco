from __future__ import unicode_literals

class State(object):

    def __init(self, state_id, items):
        self._state_id = state_id
        self._items = items

    # spec: None -> str
    @property
    def state_id(self):
        return self._state_id

    # spec: None -> {str:object}
    @property
    def items(self):
        return self._items

    _state_id = None
    _items = {}

__author__ = 'andrey.ushakov'