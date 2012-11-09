from __future__ import unicode_literals

class DataProcessor(object):

    # spec : object -> object
    def process(self, source_data, **kwargs):
        raise NotImplementedError

__author__ = 'andrey.ushakov'
