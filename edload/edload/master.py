__author__ = 'sravi'

import logging
from celery.decorators import periodic_task
from celery.schedules import crontab
from celery import Celery
from datetime import timedelta
from edload.settings.config import Config, get_setting

MASTER_SCHEDULER_HOUR = get_setting(Config.MASTER_SCHEDULER_HOUR)
MASTER_SCHEDULER_MIN = get_setting(Config.MASTER_SCHEDULER_MIN)

log = logging.getLogger('edload')

# hack till integrarion with edworker
celery = Celery('master', broker='amqp://guest@localhost//', backend='amqp')
celery.conf.CELERY_TASK_SERIALIZER = 'json'
celery.conf.CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'edload.master.start_edware_data_refresh',
        'schedule': timedelta(seconds=10),
        'args': (16, 16)
    },
}
celery.conf.CELERY_TIMEZONE = 'US/Eastern'
# hack till integrarion with edworker

@celery.task
def start_edware_data_refresh():
    print('Starting Scheduled edware data refresh task')



@periodic_task(run_every=timedelta(seconds=2))
def myPeriodicTask():
    print('periodic_task')


@periodic_task(run_every=crontab())
def myCronTask():
    print('cron_task')