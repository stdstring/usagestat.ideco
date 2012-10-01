from __future__ import unicode_literals

class LoggerHelper(object):

    # spec: bool -> str
    @staticmethod
    def bool_result_to_str(result):
        if result:
            return 'successfully'
        else:
            return 'fails'

__author__ = 'andrey.ushakov'
