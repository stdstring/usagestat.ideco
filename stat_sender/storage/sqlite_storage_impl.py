from __future__ import unicode_literals
from storage.storage import Storage

class SqliteStorageImpl(Storage):
    # spec: None -> StatData
    def get_data(self):
        raise NotImplementedError

    # spec: (int, int) -> None
    def clear(self, id_clear_range):
        raise NotImplementedError

__author__ = 'andrey.ushakov'
