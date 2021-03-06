from __future__ import unicode_literals
from collections import OrderedDict
import common.state

class FileSourceCollector(object):

    # spec: [Filter], [Handler], OrderedDict -> FileSourceCollector
    def __init__(self, filters, handlers, initial_state):
        self._filters = filters
        self._handlers = handlers
        self._initial_state = initial_state

    # spec: [str] -> {str:[object]}
    def collect(self, source):
        #noinspection PyUnresolvedReferences
        state = common.state.State(None, None, OrderedDict(self._initial_state))
        #inspection PyUnresolvedReferences
        for source_item in source:
            state = self._collect_item(source_item, state)
        return state.items

    # spec: str -> State
    def _collect_item(self, source, state):
        filtered_source = self._apply_filters(source)
        return self._apply_handler(filtered_source, state)

    # spec: str -> str
    def _apply_filters(self, source):
        changed_str = source
        for filter in self._filters:
            changed_str = filter.filter(changed_str)
        return changed_str

    # spec: str -> State
    def _apply_handler(self, source, state):
        for handler in self._handlers:
            result = handler.process(source, state)
            # result = (True|False, State)
            if result[0]:
                return result[1]
        return state

__author__ = 'andrey.ushakov'
