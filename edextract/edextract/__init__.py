# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

from apscheduler.scheduler import Scheduler
from edextract.status.status import delete_stats


def run_cron_cleanup(settings):
    '''
    Read cron scheduling entries and schedule
    '''
    cron_time = {}
    year = settings.get("extract.cleanup.schedule.cron.year")
    month = settings.get("extract.cleanup.schedule.cron.month")
    day = settings.get("extract.cleanup.schedule.cron.day")
    week = settings.get("extract.cleanup.schedule.cron.week")
    day_of_week = settings.get("extract.cleanup.schedule.cron.day_of_week")
    hour = settings.get("extract.cleanup.schedule.cron.hour")
    minute = settings.get("extract.cleanup.schedule.cron.minute")
    second = settings.get("extract.cleanup.schedule.cron.second")

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
        sched.add_cron_job(delete_stats, **cron_time)
