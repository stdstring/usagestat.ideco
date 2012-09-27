from __future__ import unicode_literals

class Storage(object):

    # spec: str, str -> bool
    def save(self, category, data):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
