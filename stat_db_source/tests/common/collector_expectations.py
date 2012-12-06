from __future__ import unicode_literals

def set_collect_data_expectations(logger, cursor, query_list, result_list):
    logger.info('collect_data(query_executer) enter')
    index = 0
    while index < len(query_list):
        logger.info('_collect_data_item({0:s}) enter'.format(query_list[index]))
        cursor.execute(query_list[index])
        cursor.fetchall().AndReturn(result_list[index])
        logger.info('_collect_data_item({0:s}) exit'.format(query_list[index]))
        index += 1
    logger.info('collect_data(query_executer) exit')

def set_process_data_expectations(logger, dest_storage, source_id, save_items_list):
    index = 0
    while index < len(save_items_list):
        logger.info('process_data() enter')
        logger.info('process_data() exit')
        dest_storage.save_data(source_id, save_items_list[index])
        index += 1

__author__ = 'andrey.ushakov'
