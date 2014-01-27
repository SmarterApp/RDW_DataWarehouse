__author__ = 'sravi'

import logging
import datetime
from celery.schedules import crontab
from celery.task import periodic_task
from edload.settings.config import Config, get_setting

MASTER_SCHEDULER_HOUR = get_setting(Config.MASTER_SCHEDULER_HOUR)
MASTER_SCHEDULER_MIN = get_setting(Config.MASTER_SCHEDULER_MIN)

log = logging.getLogger('edload')

@periodic_task(run_every=crontab(minute="*/" + MASTER_SCHEDULER_MIN))
def start_data_refresh():
    log.info("Hi from Master Scheduler At: " + str(datetime.datetime.now()))

