from __future__ import unicode_literals

class Endpoint(object):

    # spec: str -> bool
    def send(self, data):
        raise NotImplementedError

__author__ = 'andrey.ushakov'
