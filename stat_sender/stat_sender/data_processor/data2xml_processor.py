from __future__ import unicode_literals
from xml.dom.minidom import getDOMImplementation
from data_processor import DataProcessor

class Data2XmlProcessor(DataProcessor):

    # spec: str, {...} -> str (xml in str representation)
    def process(self, source_data, **kwargs):
        user_id = kwargs['user_id']
        impl = getDOMImplementation()
        doc = impl.createDocument(None, 'data_packet', None)
        packet = doc.documentElement
        packet.setAttribute('user_id', str(user_id))
        for item in source_data.stat_data_items:
            self._process_stat_data_item(doc, packet, item)
        return doc.toxml()

    # spec: Document, Element,StatDataItem -> None
    def _process_stat_data_item(self, doc, parent, item):
        data_item = doc.createElement('data_item')
        parent.appendChild(data_item)
        self._create_data_item_part(doc, data_item, 'source', item.source)
        self._create_data_item_part(doc, data_item, 'category', item.category)
        self._create_data_item_part(doc, data_item, 'timemarker', '{0:%Y-%m-%d %H:%M:%S}'.format(item.timemarker))
        self._create_data_item_part(doc, data_item, 'data', item.data)

    # spec: Document, Element, str, object -> None
    def _create_data_item_part(self, doc, data_item, name, data):
        part = doc.createElement(name)
        data_item.appendChild(part)
        part.appendChild(doc.createTextNode(str(data)))


__author__ = 'andrey.ushakov'
