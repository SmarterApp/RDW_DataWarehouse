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
