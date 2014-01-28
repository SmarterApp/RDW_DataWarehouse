__author__ = 'sravi'

import logging
from celery.decorators import periodic_task
from celery.schedules import crontab
from celery import Celery
from datetime import timedelta
from edload.settings.config import Config, get_setting
from kombu.common import Broadcast
from kombu import Exchange, Queue

MASTER_SCHEDULER_HOUR = get_setting(Config.MASTER_SCHEDULER_HOUR)
MASTER_SCHEDULER_MIN = get_setting(Config.MASTER_SCHEDULER_MIN)

log = logging.getLogger('edload')

# hack till integrarion with edworker
celery = Celery('master', broker='amqp://guest@localhost//', backend='amqp')
celery.conf.CELERY_TASK_SERIALIZER = 'json'
celery.conf.CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'edload.master.start_edware_data_refresh',
        'schedule': timedelta(seconds=30)
    },
}
celery.conf.CELERY_TIMEZONE = 'US/Eastern'
default_exchange = Exchange('default', type='direct')
celery.conf.CELERY_QUEUES = (Broadcast('edload_slaves'), Queue('edload_master', default_exchange, routing_key='default'))
celery.conf.CELERY_ROUTES = {'edload.master.slaves_get_ready_for_data_load': {'queue': 'edload_slaves'},
                             'edload.master.start_edware_data_refresh': {'queue': 'edload_master', 'routing_key': 'default'}}
celery.conf.CELERY_DEFAULT_QUEUE = 'edload_master'
celery.conf.CELERY_DEFAULT_EXCHANGE = 'default'
celery.conf.CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
celery.conf.CELERY_DEFAULT_ROUTING_KEY = 'default'
# hack till integrarion with edworker


@celery.task
def start_edware_data_refresh():
    print('Master: Starting Scheduled edware data refresh task')
    print('Master: Scheduling task for slaves to start data refresh')
    slaves_get_ready_for_data_load.delay()


@celery.task
def slaves_get_ready_for_data_load():
    print('Slave: starting to prep up for data refresh')

#@periodic_task(run_every=timedelta(seconds=2))
#def myPeriodicTask():
#    print('periodic_task')


#@periodic_task(run_every=crontab())
#def myCronTask():
#    print('cron_task')