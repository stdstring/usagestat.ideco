from __future__ import unicode_literals
from unittest.case import TestCase
from src.filter.spaces_filter import SpacesFilter

class TestSpacesFilter(TestCase):

    def test_lead_spaces(self):
        self.assertEquals('data', self._filter.filter('  data'))
        self.assertEquals('data', self._filter.filter('\t\tdata'))
        self.assertEquals('data', self._filter.filter('\t data'))

    def test_tail_spaces(self):
        self.assertEquals('data', self._filter.filter('data  '))
        self.assertEquals('data', self._filter.filter('data\t\t'))
        self.assertEquals('data', self._filter.filter('data \t'))

    def test_lead_and_tail_spaces(self):
        self.assertEquals('data', self._filter.filter('  data  '))
        self.assertEquals('data', self._filter.filter('\t\tdata\t\t'))
        self.assertEquals('data', self._filter.filter(' \tdata \t'))

    def test_internal_spaces(self):
        self.assertEquals('some  data', self._filter.filter('some  data'))
        self.assertEquals('some\t\tdata', self._filter.filter('some\t\tdata'))
        self.assertEquals('some \tdata', self._filter.filter('some \tdata'))

    _filter = SpacesFilter()

__author__ = 'andrey.ushakov'
