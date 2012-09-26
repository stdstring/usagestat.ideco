from __future__ import unicode_literals
from unittest.case import TestCase
from src.file_source_collector import FileSourceCollector
from src.filter.comment_filter import CommentFilter
from src.filter.spaces_filter import SpacesFilter
from src.handler.aggregate_key_value_handler import AggregateKeyValueHandler
from src.handler.simple_key_value_handler import SimpleKeyValueHandler
from src.handler.standard_config_section_handler import StandardConfigSectionHandler
from src.utils.standard_key_transformer import StandardKeyTransformer

class TestFileSourceCollector(TestCase):

    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName)
        key_transformer = StandardKeyTransformer()
        filters = [CommentFilter('#'), SpacesFilter()]
        handlers = [StandardConfigSectionHandler(),
                    SimpleKeyValueHandler('=', ['key13', 'key666'], key_transformer),
                    AggregateKeyValueHandler('=', ['key555', 'key999'], key_transformer, lambda old_value, item: old_value + 1, 0)]
        self._collector = FileSourceCollector(filters, handlers)

    def test_simple_collect(self):
        source =[' # first comment',
                 '\tkey13=IDDQD\t',
                 'key555=666 # BFG caliber ',
                 'key13=IDKFA # DOOM CHEAT\t\t\t',
                 '# second comment',
                 'key999=11',
                 'key555=999 # BFG some other characteristic']
        expected = {'key13': ['IDDQD', 'IDKFA'], 'key555': 2, 'key999': 1}
        actual = self._collector.collect(source)
        self.assertDictEqual(expected, actual)

    def test_sections_collect(self):
        source =[' # comment',
                 '[section_number_1]',
                 '\t # non empty section\t',
                 'key13=IDDQD\t\t\t',
                 'key555=999 # some strange value',
                 '[section_number_2]',
                 '# empty section',
                 '[section_number_3]',
                 '# nonempty section',
                 'key13=IDKFA\t\t\t',
                 'key555=777 # yet one some strange value',
                 'key555=11']
        expected = {'section_number_1.key13': ['IDDQD'], 'section_number_3.key13': ['IDKFA'], 'section_number_1.key555': 1, 'section_number_3.key555': 2}
        actual = self._collector.collect(source)
        self.assertDictEqual(expected, actual)

    def test_collect_with_skipped_items(self):
        source =[' # comment',
                 '[section_1]',
                 'key777=333',
                 'key13:999',
                 '[section_number_2',
                 '# yet one comment',
                 'key555=1111']
        expected = {'section_1.key555': 1}
        actual = self._collector.collect(source)
        self.assertDictEqual(expected, actual)

    _collector = None

__author__ = 'andrey.ushakov'
