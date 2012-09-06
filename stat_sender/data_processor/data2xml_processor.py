from __future__ import unicode_literals
from data_processor.data_processor import DataProcessor

class Data2XmlProcessor(DataProcessor):

    # spec : StatData -> str (xml in str representation)
    def process(self, source_data):
        raise NotImplementedError

__author__ = 'std_string'
