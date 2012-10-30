from __future__ import unicode_literals
from unittest.case import TestCase
from stat_file_source.filter.spaces_filter import SpacesFilter

class TestSpacesFilter(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSpacesFilter, self).__init__(methodName)
        self._filter = SpacesFilter()

    def test_lead_spaces(self):
        self.assertEqual('data', self._filter.filter('  data'))
        self.assertEqual('data', self._filter.filter('\t\tdata'))
        self.assertEqual('data', self._filter.filter('\t data'))

    def test_tail_spaces(self):
        self.assertEqual('data', self._filter.filter('data  '))
        self.assertEqual('data', self._filter.filter('data\t\t'))
        self.assertEqual('data', self._filter.filter('data \t'))

    def test_lead_and_tail_spaces(self):
        self.assertEqual('data', self._filter.filter('  data  '))
        self.assertEqual('data', self._filter.filter('\t\tdata\t\t'))
        self.assertEqual('data', self._filter.filter(' \tdata \t'))

    def test_internal_spaces(self):
        self.assertEqual('some  data', self._filter.filter('some  data'))
        self.assertEqual('some\t\tdata', self._filter.filter('some\t\tdata'))
        self.assertEqual('some \tdata', self._filter.filter('some \tdata'))

__author__ = 'andrey.ushakov'
