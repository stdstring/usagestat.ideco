from __future__ import unicode_literals
import unittest

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
