from __future__ import unicode_literals
from datetime import datetime

# spec: str -> datetime
def str_2_time(source_str):
    return datetime.strptime(source_str, '%Y-%m-%d %H:%M:%S')

__author__ = 'andrey.ushakov'
