from __future__ import unicode_literals
from src.filter.filter import Filter

class SpacesFilter(Filter):

    # spec: str -> str
    def filter(self, source):
        return source.strip()

__author__ = 'andrey.ushakov'
