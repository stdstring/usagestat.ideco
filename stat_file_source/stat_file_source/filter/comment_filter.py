from __future__ import unicode_literals
from stat_file_source.filter.filter import Filter

class CommentFilter(Filter):

    # spec: str -> CommentFilter
    def __init__(self, comment_leader='#'):
        self._comment_leader = comment_leader

    # spec: str -> str
    def filter(self, source):
        find_result = self._find_comment_start(source)
        if find_result > -1:
            return source[0:find_result]
        else:
            return source

    # spec: str -> int
    def _find_comment_start(self, source):
        # TODO (andrey.ushakov) : some comment leaders may be escaped
        return source.find(self._comment_leader)

__author__ = 'andrey.ushakov'
