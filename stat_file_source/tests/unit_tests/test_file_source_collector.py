from __future__ import unicode_literals
from collections import OrderedDict
from unittest.case import TestCase
from stat_file_source.file_source_collector import FileSourceCollector
from stat_file_source.filter.comment_filter import CommentFilter
from stat_file_source.filter.spaces_filter import SpacesFilter
from stat_file_source.handler.aggregate_key_value_handler import AggregateKeyValueHandler
from stat_file_source.handler.simple_key_list_handler import SimpleKeyListHandler
from stat_file_source.handler.standard_config_section_handler import StandardConfigSectionHandler
from stat_file_source.utils.standard_key_transformer import StandardKeyTransformer

class TestFileSourceCollector(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestFileSourceCollector, self).__init__(methodName)
        key_transformer = StandardKeyTransformer()
        ip_key_transformer = lambda key, value, state: state.state_id + '_ip'
        aggregate_fun = lambda old_value, item: old_value + 1
        filters = [CommentFilter('#'), SpacesFilter()]
        handlers = [StandardConfigSectionHandler(),
                    SimpleKeyListHandler.create_with_known_key_list('=', ['key13', 'key666'], key_transformer),
                    AggregateKeyValueHandler.create_with_known_key_list('=', ['key555', 'key999'], key_transformer, aggregate_fun, 0),
                    AggregateKeyValueHandler.create_with_known_key_list('=', ['ip0', 'ip1', 'ip2', 'ip3', 'ip4'], ip_key_transformer, aggregate_fun, 0)]
        self._collector = FileSourceCollector(filters, handlers, OrderedDict())

    def test_simple_collect(self):
        source =[' # first comment',
                 '\tkey13=IDDQD\t',
                 'key555=666 # BFG caliber ',
                 'key13=IDKFA # DOOM CHEAT\t\t\t',
                 '# second comment',
                 'key999=11',
                 'key555=999 # BFG some other characteristic']
        expected = OrderedDict([('key13', ['IDDQD', 'IDKFA']), ('key555', 2), ('key999', 1)])
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
        expected = OrderedDict([('section_number_1.key13', ['IDDQD']), ('section_number_1.key555', 1), ('section_number_3.key13', ['IDKFA']), ('section_number_3.key555', 2)])
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
        expected = OrderedDict([('section_1.key555', 1)])
        actual = self._collector.collect(source)
        self.assertDictEqual(expected, actual)

    def test_collect_with_aggegate_by_one_key(self):
        source =[' # comment',
                 '[gate]',
                 'ip0=192.168.0.1',
                 'ip1=192.168.0.2',
                 '[dns]',
                 'ip0=192.168.100.1',
                 'ip1=192.168.101.1',
                 'ip2=192.168.122.2',
                 'ip9=192.168.166.66',
                 '[wins]',
                 'ip0=192.168.111.11']
        expected = OrderedDict([('gate_ip', 2), ('dns_ip', 3), ('wins_ip', 1)])
        actual = self._collector.collect(source)
        self.assertDictEqual(expected, actual)

__author__ = 'andrey.ushakov'
