from __future__ import unicode_literals
import unittest
from stat_life_cycle_test_scenario import StatLifeCycleTestScenario

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(StatLifeCycleTestScenario))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
