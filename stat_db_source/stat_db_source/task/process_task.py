from __future__ import unicode_literals

# TODO (andrey.ushakov) : make this class abstract
class ProcessTask(object):

    # spec: [[(...)]] -> [DataItem]
    def process(self, intermediate_data):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
