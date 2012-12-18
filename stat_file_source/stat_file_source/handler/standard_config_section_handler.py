from __future__ import unicode_literals
import re
from stat_file_source.common.state import State
from stat_file_source.handler.handler import Handler

class StandardConfigSectionHandler(Handler):

    def __init__(self):
        self._rexpr = re.compile('\[(?P<section_name>.+)\]')

    # spec: str, State -> (bool, State)
    def process(self, source, state):
        #result = re.match('\[(?P<section_name>.+)\]', source)
        result = self._rexpr.match(source)
        if result is None:
            return (False, state)
        else:
            section_name = result.group('section_name')
            return (True, State(section_name, section_name, state.items))

__author__ = 'andrey.ushakov'
