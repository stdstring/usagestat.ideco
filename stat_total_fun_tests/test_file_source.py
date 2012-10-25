from __future__ import unicode_literals
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_file_source'))
#noinspection PyUnresolvedReferences
from stat_file_source.file_source_collect_task import FileSourceCollectTask
#noinspection PyUnresolvedReferences
from stat_file_source.filter.comment_filter import CommentFilter
#noinspection PyUnresolvedReferences
from stat_file_source.filter.spaces_filter import SpacesFilter
#noinspection PyUnresolvedReferences
from stat_file_source.handler.standard_config_section_handler import StandardConfigSectionHandler
#noinspection PyUnresolvedReferences
from stat_file_source.handler.simple_key_value_handler import SimpleKeyValueHandler
#noinspection PyUnresolvedReferences
from stat_file_source.handler.transform_key_value_handler import TransformKeyValueHandler
#noinspection PyUnresolvedReferences
from stat_file_source.handler.aggregate_key_value_handler import AggregateKeyValueHandler
#noinspection PyUnresolvedReferences
from stat_file_source.utils.standard_key_transformer import StandardKeyTransformer

# spec: str -> str
def transform_user_fun(source_value):
    delimiter_index = source_value.find(',')
    if delimiter_index == -1:
        return source_value
    else:
        user = source_value[0:delimiter_index]
        pwd = '*' * (len(source_value) - delimiter_index - 1)
        return '%(user)s,%(pwd)s' % {'user': user, 'pwd': pwd}

class TestFileSource(object):

    def __init__(self, source_filename, db_file_path, logger):
        filters = [CommentFilter('#'), SpacesFilter()]
        standard_key_transformer = StandardKeyTransformer()
        ip_key_transformer = lambda key, state: '%(category)s.ip' % {'category': state.state_id}
        handlers = [StandardConfigSectionHandler(),
                    SimpleKeyValueHandler.create_with_known_key_predicate('=', lambda key, state: state.state_id == 'services', standard_key_transformer),
                    TransformKeyValueHandler.create_with_known_key_predicate('=', lambda key, state: state.state_id == 'users', standard_key_transformer, transform_user_fun),
                    AggregateKeyValueHandler.create_with_known_key_list('=', ['ip0', 'ip1', 'ip2', 'ip3', 'ip4'], ip_key_transformer, lambda old_value, item: old_value + 1, 0)]
        self._collect_task = FileSourceCollectTask(self._source, filters, handlers, source_filename, db_file_path, logger)

    def collect_stat_data(self):
        self._collect_task.execute()

    _source = 'file_source'

__author__ = 'andrey.ushakov'
