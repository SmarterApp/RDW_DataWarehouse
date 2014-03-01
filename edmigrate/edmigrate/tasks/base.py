'''
Created on Feb 28, 2014

@author: dip
'''
from celery import Task
from edcore.database.utils.constants import UdlStatsConstants
from edcore.database.utils.query import update_udl_stats


class BaseTask(Task):
    '''
    Base Task for Celery Tasks
    '''
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Write to udl stats table on exceptions
        # TODO:  get batch_guid
        batch_guid = 'temp'
        update_udl_stats(batch_guid, {UdlStatsConstants.LOAD_STATUS: UdlStatsConstants.STATUS_FAILED})
