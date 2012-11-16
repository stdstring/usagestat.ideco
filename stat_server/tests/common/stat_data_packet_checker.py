from __future__ import unicode_literals

def check_stat_data_packet(test_case, expected, actual):
    test_case.assertIsNotNone(actual)
    test_case.assertEqual(expected.user_id, actual.user_id)
    test_case.assertIsNotNone(actual.items)
    test_case.assertEqual(len(expected.items), len(actual.items))
    index = 0
    while index < len(expected.items):
        check_stat_data_item(test_case, expected.items[index], actual.items[index])
        index += 1

def check_stat_data_item(test_case, expected, actual):
    test_case.assertIsNotNone(actual)
    test_case.assertEqual(expected.source, actual.source)
    test_case.assertEqual(expected.category, actual.category)
    test_case.assertEqual(expected.timemarker, actual.timemarker)
    test_case.assertEqual(expected.data, actual.data)

__author__ = 'andrey.ushakov'
