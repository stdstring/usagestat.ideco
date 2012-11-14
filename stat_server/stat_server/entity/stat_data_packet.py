from __future__ import unicode_literals
import uuid
from stat_server.common.datetime_converters import str_2_time
from stat_server.entity.stat_data_item import StatDataItem

class StatDataPacket(object):

    # spec: UUID, [StatDataItem] -> StatDataPacket
    def __init__(self, user_id=None, items=None):
        self._user_id = user_id
        self._items = items

    # spec: None -> UUID
    @property
    def user_id(self):
        return self._user_id

    # spec: UUID -> None
    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    # spec: None -> [StatDataItem]
    @property
    def items(self):
        return self._items

    # spec: [StatDataItem] -> None
    @items.setter
    def items(self, value):
        self._items = value

    def __str__(self):
        items = ','.join(map(lambda item: str(item), self.items))
        return 'StatDataPacket(user_id="{user_id:s}", items=[{items:s}])'.format(user_id=self.user_id, items=items)

    def __repr__(self):
        return self.__str__()

    # spec: {...} -> StatDataPacket
    @staticmethod
    def create(internal_repr):
        # source: <data_packet user_id="83cf01c6-2284-11e2-9494-08002703af71"><data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item></data_packet>
        # repr: {'data_packet': {'user_id': '83cf01c6-2284-11e2-9494-08002703af71', 'data_item': [{'source': {'': 'source1'}, 'category': {'': 'cat1'}, 'timemarker': {'': '2012-12-21 23:59:59'}, 'data': {'': 'IDDQD'}}]}}
        packet_body = internal_repr['data_packet']
        user_id = uuid.UUID(packet_body['user_id'])
        data_items_body = packet_body['data_item']
        if not isinstance(data_items_body, list):
            data_items_body = [data_items_body]
        data_item_storage = []
        for data_item_body in data_items_body:
            source = data_item_body['source']['']
            category = data_item_body['category']['']
            timemarker = str_2_time(data_item_body['timemarker'][''])
            data = data_item_body['data']['']
            data_item_storage.append(StatDataItem(source, category, timemarker, data))
        return StatDataPacket(user_id, data_item_storage)

__author__ = 'andrey.ushakov'
