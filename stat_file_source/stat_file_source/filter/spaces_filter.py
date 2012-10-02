from __future__ import unicode_literals
from stat_file_source.filter.filter import Filter

class SpacesFilter(Filter):

    # spec: str -> str
    def filter(self, source):
        return source.strip()

__author__ = 'andrey.ushakov'
