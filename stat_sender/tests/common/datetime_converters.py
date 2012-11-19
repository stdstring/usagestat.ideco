from __future__ import unicode_literals

# spec: datetime -> str
def datetime_2_str(source):
    return source.strftime('%Y-%m-%d %H:%M:%S')

__author__ = 'andrey.ushakov'
