'''
Created on Apr 28, 2014

@author: dip
'''
from edudl2.udl2.celery import celery


@celery.task(name="udl2.W_task_utils.handle_group_results")
def handle_group_results(msgs):
    '''
    Return the last msg in the group of tasks
    :param list msgs: list of results from group tasks
    '''
    return msgs[len(msgs) - 1] if msgs else {}
