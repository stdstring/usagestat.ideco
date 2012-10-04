from __future__ import unicode_literals
from data_processor import DataProcessor

class Data2XmlProcessor(DataProcessor):

    # spec : StatData -> str (xml in str representation)
    def process(self, source_data):
        result = {}
        for data_item in source_data.stat_data_items:
            source = data_item.source
            category = data_item.category
            if source not in result:
                result[source] = {}
            if category not in result[source]:
                result[source][category] = []
            result[source][category].append(self._convert_stat_data_item(data_item))
        return self._create_result_xml(result)

    # spec: {str: {str: [str]}} -> str (xml in str representation)
    def _create_result_xml(self, aggregated_data):
        source_storage = []
        for source in aggregated_data:
            category_storage = []
            for category in aggregated_data[source]:
                category_internal_data = ''.join(aggregated_data[source][category])
                category_data = '<%(category)s>%(data)s</%(category)s>' % {'category':category, 'data':category_internal_data}
                category_storage.append(category_data)
            source_internal_data = ''.join(category_storage)
            source_data = '<%(source)s>%(data)s</%(source)s>' % {'source':source, 'data':source_internal_data}
            source_storage.append(source_data)
        total_data = ''.join(source_storage)
        return '<stat_data>%(data)s</stat_data>' % {'data': total_data}

    # spec : StatDataItem -> str (xml in str representation)
    def _convert_stat_data_item(self, item):
        return '<item><timemarker>%(timemarker)s</timemarker><data>%(data)s</data></item>' %\
               {'timemarker':str(item.timemarker), 'data':item.data}

__author__ = 'andrey.ushakov'
