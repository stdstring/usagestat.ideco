from __future__ import unicode_literals
import unittest
from stat_life_cycle_scenario import StatLifeCycleScenario

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(StatLifeCycleScenario))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
