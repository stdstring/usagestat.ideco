from __future__ import unicode_literals
from data_processor import DataProcessor

class Data2XmlProcessor(DataProcessor):

    # spec : StatData -> str (xml in str representation)
    def process(self, source_data):
        storage = []
        for item in source_data.stat_data_items:
            storage.append(self._process_stat_data_item(item))
        inner_content = ''.join(storage)
        return '<objects>{0:s}</objects>'.format(inner_content)

    # spec : StatDataItem -> str (xml in str representation)
    def _process_stat_data_item(self, item):
        format_str = '<object>' \
                     '<source>{source:s}</source>' \
                     '<category>{category:s}</category>' \
                     '<timemarker>{timemarker:%Y-%m-%d %H:%M:%S}</timemarker>' \
                     '<data>{data:s}</data>' \
                     '</object>'
        return format_str.format(source = item.source, category = item.category, timemarker = item.timemarker, data = str(item.data))

__author__ = 'andrey.ushakov'
