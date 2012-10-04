from __future__ import unicode_literals

class Storage(object):
    # spec: None -> [(int, str, str, str, str)]
    def get_data(self):
        raise NotImplementedError

    # spec: (int, int) -> None
    def clear(self, id_clear_range):
        raise NotImplementedError

__author__ = 'andrey.ushakov'
