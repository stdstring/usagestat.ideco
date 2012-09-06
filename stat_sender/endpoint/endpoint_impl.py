from __future__ import unicode_literals
from endpoint.endpoint import EndPoint

class EndPointImpl(EndPoint):

    # spec: str -> bool
    def send(self, data):
        raise NotImplementedError

__author__ = 'andrey.ushakov'
