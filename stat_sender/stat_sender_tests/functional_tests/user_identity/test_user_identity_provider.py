from __future__ import unicode_literals
import os
from unittest.case import TestCase
from stat_sender.user_identity.user_identity_provider import UserIdentityProvider

class TestUserIdentityProvider(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestUserIdentityProvider, self).__init__(methodName)
        self._existing_user_identity_source = os.path.abspath('stat_sender_tests/functional_tests/user_identity/user.id')
        self._nonexisting_user_identity_source = os.path.abspath('stat_sender_tests/functional_tests/user_identity/user2.id')

    def tearDown(self):
        if os.path.exists(self._nonexisting_user_identity_source):
            os.unlink(self._nonexisting_user_identity_source)

    def test_user_identity_source_exists(self):
        self.assertTrue(os.path.exists(self._existing_user_identity_source))
        user_identity_provider = UserIdentityProvider(self._existing_user_identity_source)
        user_identity = user_identity_provider.get_user_identity()
        self.assertEqual('83cf01c6-2284-11e2-9494-08002703af71', str(user_identity))
        self.assertTrue(os.path.exists(self._existing_user_identity_source))

    def test_user_identity_source_nonexists(self):
        self.assertFalse(os.path.exists(self._nonexisting_user_identity_source))
        user_identity_provider = UserIdentityProvider(self._nonexisting_user_identity_source)
        user_identity = user_identity_provider.get_user_identity()
        self.assertNotEqual('83cf01c6-2284-11e2-9494-08002703af71', str(user_identity))
        self.assertTrue(os.path.exists(self._nonexisting_user_identity_source))

__author__ = 'andrey.ushakov'
