from __future__ import unicode_literals

class Storage(object):

    # spec: StatDataPacket -> bool
    def save_data(self, data):
        raise NotImplementedError()


__author__ = 'andrey.ushakov'
