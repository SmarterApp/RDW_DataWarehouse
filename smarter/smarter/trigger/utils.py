'''
Created on Jun 24, 2013

@author: dip
'''
from apscheduler.scheduler import Scheduler
import logging
from edauth.utils import to_bool


logger = logging.getLogger('smarter')


def run_cron_job(settings, prefix, job):
    '''
    Runs a cron job

    :param dict settings:  configuration for the application
    :param string prefix:  the prefix to prepend to properties
    :param job: reference to the function to run as a cron job
    '''
    enabled = to_bool(settings.get(prefix + "enable", 'False'))
    if enabled:
        new_prefix = prefix + 'schedule.cron.'
        cron_time = {}
        year = settings.get(new_prefix + "year")
        month = settings.get(new_prefix + "month")
        day = settings.get(new_prefix + "day")
        week = settings.get(new_prefix + "week")
        day_of_week = settings.get(new_prefix + "day_of_week")
        hour = settings.get(new_prefix + "hour")
        minute = settings.get(new_prefix + "minute")
        second = settings.get(new_prefix + "second")

        if year is not None:
            cron_time['year'] = year
        if month is not None:
            cron_time['month'] = month
        if day is not None:
            cron_time['day'] = day
        if week is not None:
            cron_time['week'] = week
        if day_of_week is not None:
            cron_time['day_of_week'] = day_of_week
        if hour is not None:
            cron_time['hour'] = hour
        if minute is not None:
            cron_time['minute'] = minute
        if second is not None:
            cron_time['second'] = second
        if len(cron_time) > 0:
            sched = Scheduler()
            sched.start()
            logger.info('cron job is added for ' + prefix)
            sched.add_cron_job(job, args=[settings], **cron_time)
