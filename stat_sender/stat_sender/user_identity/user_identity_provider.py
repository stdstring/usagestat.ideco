from __future__ import unicode_literals
import os
import uuid

class UserIdentityProvider(object):

    def __init__(self, user_identity_source):
        self._user_identity = None
        self._user_identity_source = user_identity_source

    def get_user_identity(self):
        if self._user_identity is None:
            self._user_identity = self._read_user_identity()
        return self._user_identity

    def _read_user_identity(self):
        if os.path.exists(self._user_identity_source):
            user_identity = uuid.UUID(self._read_from_source())
        else:
            user_identity = uuid.uuid1()
            self._create_source(str(user_identity))
        return user_identity

    def _read_from_source(self):
        with open(self._user_identity_source, 'r') as source:
            return source.read()

    def _create_source(self, user_identity):
        with open(self._user_identity_source, 'w') as source:
            return source.write(user_identity)

__author__ = 'andrey.ushakov'