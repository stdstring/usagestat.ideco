from __future__ import unicode_literals
from unittest.case import TestCase
from stat_file_source.filter.comment_filter import CommentFilter

class TestCommentFilter(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCommentFilter, self).__init__(methodName)
        self._filter = CommentFilter('#')

    def test_without_comment(self):
        self.assertEqual('some line with data', self._filter.filter('some line with data'))

    def test_whole_line_comment(self):
        self.assertEqual('', self._filter.filter('# some line with comment'))

    def test_line_end_comment(self):
        self.assertEqual('some line with data ', self._filter.filter('some line with data # some line with comment'))

__author__ = 'andrey.ushakov'
