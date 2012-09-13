from __future__ import unicode_literals
import sys
from src import stat_sender_entry_point

def main():
    result = stat_sender_entry_point.execute()
    if not result:
        sys.exit(-1)

if __name__ == '__main__':
    main()

__author__ = 'andrey.ushakov'
