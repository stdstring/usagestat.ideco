from __future__ import unicode_literals

class Filter(object):

    # spec: str -> str
    def filter(self, source):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
