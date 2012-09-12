from __future__ import unicode_literals

class EndPoint(object):

    # spec: str -> bool
    def send(self, data):
        raise NotImplementedError

__author__ = 'andrey.ushakov'
