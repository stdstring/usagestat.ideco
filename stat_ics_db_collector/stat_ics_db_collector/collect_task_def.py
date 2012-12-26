from __future__ import unicode_literals
from stat_db_source.task.collect_task import CollectTask
from stat_db_source.task.transform_process_task import TransformProcessTask

def _create_license_type_collect_task():
    license_type_dict = {4: 'Standard Named', 5: 'Enterprise Named', 6: 'Standard Concurrent', 7: 'Enterprise Concurrent', None: 'Trial'}
    query = 'SELECT REG_VER FROM REG'
    process_task = TransformProcessTask(lambda row: 'license.Type', lambda row: license_type_dict[row[0]])
    return CollectTask([query], process_task)

def _create_user_count_collect_task():
    # count enabled and disabled users
    query = 'SELECT COUNT(ID) FROM USERS WHERE END_USER=1 AND SERVER=0 AND DELETED=0'
    process_task = TransformProcessTask(lambda row: 'users.EndUserCount', lambda row: row[0])
    return CollectTask([query], process_task)

def _create_user_with_agent_auth_count_collect_task():
    # count enabled and disabled users
    query = 'SELECT COUNT(ID) FROM USERS WHERE END_USER=1 AND SERVER=0 AND DELETED=0 AND (AUTH_TYPE=2 OR AUTH_TYPE=3)'
    process_task = TransformProcessTask(lambda row: 'users.EndUserWithAgentAuthCount', lambda row: row[0])
    return CollectTask([query], process_task)

def _create_ad_sync_collect_task():
    ENABLED = 'enabled'
    DISABLED = 'disabled'
    query = 'SELECT COUNT(ID) FROM USERS WHERE END_USER=0 AND SERVER=0 AND DELETED=0 AND AD_IS=1'
    data_transform_fun = lambda row: ENABLED if row[0] > 0 else DISABLED
    process_task = TransformProcessTask(lambda row: 'ad.ADSync', data_transform_fun)
    return CollectTask([query], process_task)

def _create_ad_user_count_collect_task():
    query = 'SELECT COUNT(ID) FROM USERS WHERE END_USER=1 AND SERVER=0 AND DELETED=0 AND AD_IS=1'
    process_task = TransformProcessTask(lambda row: 'ad.EndUserCount', lambda row: row[0])
    return CollectTask([query], process_task)

collect_task_def = [_create_license_type_collect_task(),
                    _create_user_count_collect_task(),
                    _create_user_with_agent_auth_count_collect_task(),
                    _create_ad_sync_collect_task(),
                    _create_ad_user_count_collect_task()]

__author__ = 'andrey.ushakov'
