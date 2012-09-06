from __future__ import unicode_literals
from data_processor.data_processor import DataProcessor

class Data2XmlProcessor(DataProcessor):

    # spec : StatData -> str (xml in str representation)
    def process(self, source_data):
        result = {}
        for data_item in source_data.stat_data_items:
            if data_item.category not in result:
                result[data_item.category] = []
            result[data_item.category].append(self._convert_stat_data_item(data_item))
        return self._create_result_xml(result)

    def _create_result_xml(self, data_items_dict):
        category_data_storage = []
        for category in data_items_dict:
            category_data = '<%(category)s>%(data)s</%(category)s>' %\
                            {'category':category, 'data':data_items_dict[category]}
            category_data_storage.append(category_data)
        total_data = ''.join(category_data_storage)
        return '<stat_data>%(data)s</stat_data>' % {'data':total_data}

    # spec : SataDataItem -> str (xml in str representation)
    def _convert_stat_data_item(self, item):
        return '<%(category)s_item><timemarker>%(timemarker)s</timemarker><data>%(data)s</data></%(category)s_item>' %\
               {'category':item.category, 'timemarker':item.timemarker, 'data':item.data}

__author__ = 'std_string'
