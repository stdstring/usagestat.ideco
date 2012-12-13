from __future__ import unicode_literals
import json
from stat_source_common.entity.data_item import DataItem

def deserialize(json_str):
    # expected format: data = {'source_id': source_id_str, 'items': [{'category':  category_str, 'data': data_str}]}
    data = json.loads(json_str)
    source_id = data['source_id']
    items = data['items']
    data_item_list = map(lambda item: DataItem(item['category'], item['data']), items)
    return (source_id, data_item_list)

__author__ = 'andrey.ushakov'
