__author__ = 'sravi'

import logging
from edmigrate.celery_dev import celery
log = logging.getLogger('edmigrate.slave')


@celery.task(name='task.edmigrate.slave.slaves_get_ready_for_data_migrate', ignore_result=True)
def slaves_get_ready_for_data_migrate():
    print('Slave: starting to prep up for data refresh')
    return "Ack from slave"


@celery.task(name='task.edmigrate.slave.slaves_switch', ignore_result=True)
def slaves_switch():
    print('Slave: starting to switch')


@celery.task(name='task.edmigrate.slave.slaves_end_data_migrate', ignore_result=True)
def slaves_end_data_migrate():
    print('Slave: Ending data migration')
