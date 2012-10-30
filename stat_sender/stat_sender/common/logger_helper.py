from __future__ import unicode_literals

# spec: bool -> str
def bool_result_to_str(result):
    if result:
        return 'successfully'
    else:
        return 'fails'

__author__ = 'andrey.ushakov'
