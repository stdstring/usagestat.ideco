from __future__ import unicode_literals
import re
from src.common.state import State
from src.handler.handler import Handler

class StandardConfigSectionHandler(Handler):

    # spec: str, State -> (bool, State)
    def process(self, source, state):
        result = re.match('\[(?P<section_name>.+)\]', source)
        if result is None:
            return (False, state)
        else:
            section_name = result.group('section_name')
            return (True, State(section_name, section_name, state.items))

__author__ = 'andrey.ushakov'
