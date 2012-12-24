from __future__ import unicode_literals
from stat_file_source.filter.comment_filter import CommentFilter
from stat_file_source.filter.spaces_filter import SpacesFilter

filters_def = [CommentFilter('#'), SpacesFilter()]

__author__ = 'andrey.ushakov'