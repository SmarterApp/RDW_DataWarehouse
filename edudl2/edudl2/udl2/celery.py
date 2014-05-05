from __future__ import absolute_import
from celery import Celery
from kombu import Exchange, Queue
import os
from edcore.database.stats_connector import StatsDBConnection
import edcore.database as edcoredb
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.database.udl2_connector import initialize_db_target, initialize_db_udl, initialize_db_prod
from celery.loaders.base import BaseLoader


class UDL2CeleryLoader(BaseLoader):
    def on_worker_process_init(self):
        '''
        This method is called when a child process starts.
        '''
        # init db engine
        initialize_db_udl(udl2_conf)
        initialize_db_target(udl2_conf)
        initialize_db_prod(udl2_conf)
        # using edcore connection class to init statsdb connection
        # this needs a flat config file rather than udl2 which needs nested config
        edcoredb.initialize_db(StatsDBConnection, udl2_flat_conf, allow_schema_create=True)


def setup_udl2_queues(conf):
    queues = {}
    # set up default queues, which is always celery
    queues['default'] = Queue('celery',
                              Exchange(conf['celery_defaults']['CELERY_DEFAULT_EXCHANGE'],
                                       conf['celery_defaults']['CELERY_DEFAULT_EXCHANGE']),
                              routing_key=conf['celery_defaults']['CELERY_DEFAULT_ROUTING_KEY'])
    return queues


def setup_celery_conf(udl2_conf, celery, udl_queues):
    celery.conf.update(CELERY_TASK_RESULT_EXPIRES=10,  # TTL for results
                       CELERYD_CONCURRENCY=10,  # number of available workers processes
                       CELERY_SEND_EVENTS=True,  # send events for monitor
                       CELERY_DEFAULT_QUEUE='celery',
                       CELERY_DEFAULT_EXCHANGE='direct',
                       CELERY_DEFAULT_ROUTING_KEY='celery',
                       CELERYD_LOG_DEBUG=udl2_conf['logging']['debug'],
                       CELERYD_LOG_LEVEL=udl2_conf['logging']['level'],
                       CELERYD_LOG_FILE=udl2_conf['logging']['audit'],
                       CELERY_QUEUES=tuple(udl_queues.values()))
    return celery


# import configuration after getting path from environment variable due to celery command don't take extra options
# if UDL2_CONF is not set, use default configurations

try:
    config_path_file = os.environ['UDL2_CONF']
except Exception:
    config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE

# get udl2 configuration as nested and flat dictionary
# TODO: Refactor to use either flat or map structure
udl2_conf, udl2_flat_conf = read_ini_file(config_path_file)

# the celery instance has to be named as celery due to celery driver looks for this object in celery.py
# this is the default protocol between celery system and our implementation of tasks.

celery = Celery(loader=UDL2CeleryLoader,
                udl2_conf['celery']['root'],
                broker=udl2_conf['celery']['broker'],
                backend=udl2_conf['celery']['backend'],
                include=udl2_conf['celery']['include'])

# Create all queues entities to be use by task functions
udl2_queues = setup_udl2_queues(udl2_conf)
celery = setup_celery_conf(udl2_conf, celery, udl2_queues)

# TODO: Change udl2 to use edcore connection class for all connections


if __name__ == '__main__':
    celery.start()
