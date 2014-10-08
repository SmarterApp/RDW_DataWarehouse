'''
Created on Oct 8, 2014

@author: tosako
'''
from edudl2.udl2 import message_keys as mk, W_load_sr_integration_to_target,\
    W_load_from_integration_to_star, W_tasks_utils
from edcore.database.utils.constants import LoadType, AssessmentType


def get_tasks_by_type(msg):
    load_type = msg[mk.LOAD_TYPE]
    assessment_type = msg[mk.ASSESSMENT_TYPE]
    tasks = []
    if load_type == LoadType.STUDENT_REGISTRATION:
        tasks.append(W_load_sr_integration_to_target.task.s())
    elif load_type == LoadType.ASSESSMENT:
        if assessment_type == AssessmentType.INTERIM_ASSESSMENTS_BLOCKS:
            tasks.append(W_load_from_integration_to_star.get_explode_to_tables_tasks(msg, 'fact_block'))
            tasks.append(W_tasks_utils.handle_group_results.s())
            tasks.append(W_load_from_integration_to_star.handle_deletions.s())
        else:
            tasks.append(W_load_from_integration_to_star.get_explode_to_tables_tasks(msg, 'dim'))
            tasks.append(W_tasks_utils.handle_group_results.s())
            tasks.append(W_load_from_integration_to_star.handle_record_upsert.s())
            tasks.append(W_load_from_integration_to_star.get_explode_to_tables_tasks(msg, 'fact_asmt'))
            tasks.append(W_tasks_utils.handle_group_results.s())
            tasks.append(W_load_from_integration_to_star.handle_deletions.s())
    return tasks
