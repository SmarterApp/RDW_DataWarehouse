'''
Created on Jun 24, 2013

@author: dip
'''
from apscheduler.scheduler import Scheduler
import logging


logger = logging.getLogger('smarter')


def run_cron_job(settings, prefix, job):
    '''
    Runs a cron job

    :param dict settings:  configuration for the application
    :param string prefix:  the prefix to prepend to properties
    :param job: reference to the function to run as a cron job
    '''
    enabled = settings.get(prefix + "enable", False)
    if enabled:
        cron_time = {}
        year = settings.get(prefix + "schedule.cron.year")
        month = settings.get(prefix + "schedule.cron.month")
        day = settings.get(prefix + "schedule.cron.day")
        week = settings.get(prefix + "schedule.cron.week")
        day_of_week = settings.get(prefix + "schedule.cron.day_of_week")
        hour = settings.get(prefix + "schedule.cron.hour")
        minute = settings.get(prefix + "schedule.cron.minute")
        second = settings.get(prefix + "schedule.cron.second")

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
