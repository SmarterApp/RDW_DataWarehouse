__author__ = 'sravi'

import logging
from celery.decorators import periodic_task
from celery.schedules import crontab
from celery import Celery
from edmigrate.settings.config import Config, get_setting
from kombu.common import Broadcast
from kombu import Exchange, Queue

MASTER_SCHEDULER_HOUR = get_setting(Config.MASTER_SCHEDULER_HOUR)
MASTER_SCHEDULER_MIN = get_setting(Config.MASTER_SCHEDULER_MIN)

log = logging.getLogger('edmigrate')

# hack till integrarion with edworker
celery = Celery('master', broker='amqp://guest@localhost//', backend='amqp', include=['edmigrate.tasks.master', 'edmigrate.tasks.slave'])
celery.conf.CELERY_TASK_SERIALIZER = 'json'
celery.conf.CELERYBEAT_SCHEDULE = {
    'migrate-data-to-edware-star': {
        'task': 'task.edmigrate.master.start_edware_data_refresh',
        'schedule': crontab()
    },
}
celery.conf.CELERY_TIMEZONE = 'US/Eastern'
default_exchange = Exchange('default', type='direct')
celery.conf.CELERY_QUEUES = (Broadcast('edload_slaves'), Queue('edload_master', default_exchange, routing_key='default'))
#celery.conf.CELERY_QUEUES = (Queue('edload_slaves', default_exchange, routing_key='slave'), Queue('edload_master', default_exchange, routing_key='default'))
celery.conf.CELERY_ROUTES = {'task.edmigrate.slave.slaves_get_ready_for_data_migrate': {'queue': 'edload_slaves'},
                             'task.edmigrate.slave.slaves_switch': {'queue': 'edload_slaves'},
                             'task.edmigrate.slave.slaves_end_data_migrate': {'queue': 'edload_slaves' },
                             'task.edmigrate.master.start_edware_data_refresh': {'queue': 'edload_master', 'routing_key':'default'},
                             'task.edmigrate.master.migrate_data': {'queue': 'edload_master', 'routing_key':'default'},
                             'task.edmigrate.master.verify_master_slave_repl_status': {'queue': 'edload_master', 'routing_key':'default'}}
celery.conf.CELERY_DEFAULT_QUEUE = 'edload_master'
celery.conf.CELERY_DEFAULT_EXCHANGE = 'default'
celery.conf.CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
celery.conf.CELERY_DEFAULT_ROUTING_KEY = 'default'
# hack till integrarion with edworker