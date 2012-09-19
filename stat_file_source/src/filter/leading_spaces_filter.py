from __future__ import unicode_literals
from src.filter.filter import Filter

class LeadingSpacesFilter(Filter):

    # spec: str -> str
    def filter(self, source):
        index = 0
        while index < len(source):
            if not source[index].isspace():
                break
            index += 1
        if index == len(source):
            return source
        else:
            return source[index:len(source) - index]

__author__ = 'andrey.ushakov'
