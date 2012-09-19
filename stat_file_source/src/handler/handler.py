from __future__ import unicode_literals

class Handler(object):

    # spec: str, State -> (bool, State)
    def process(self, data_portion, state):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
