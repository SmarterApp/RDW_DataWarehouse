from __future__ import absolute_import
from celery import Celery
from kombu import Exchange, Queue
import os
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.database.udl2_connector import initialize_all_db
from celery.loaders.base import BaseLoader


class UDL2CeleryLoader(BaseLoader):
    def on_worker_process_init(self):
        '''
        This method is called when a child process starts.
        '''
        initialize_all_db(udl2_conf, udl2_flat_conf)


def configure_celery(conf, celery):
    queues = {}
    # set up default queues, which is always celery
    queues['default'] = Queue(conf['celery_defaults']['CELERY_DEFAULT_QUEUE'],
                              Exchange(conf['celery_defaults']['CELERY_DEFAULT_EXCHANGE'],
                                       conf['celery_defaults']['CELERY_DEFAULT_EXCHANGE']),
                              routing_key=conf['celery_defaults']['CELERY_DEFAULT_ROUTING_KEY'])

    celery.conf.update(CELERYD_CONCURRENCY=conf['celery_defaults']['CELERYD_CONCURRENCY'],  # number of available workers processes
                       CELERYD_LOG_DEBUG=conf['logging']['debug'],
                       CELERYD_LOG_LEVEL=conf['logging']['level'],
                       CELERYD_LOG_FILE=conf['logging']['audit'],
                       CELERY_QUEUES=tuple(queues.values()))
    celery.conf["CELERY_ALWAYS_EAGER"] = True
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

celery = Celery(udl2_conf['celery']['root'],
                broker=udl2_conf['celery']['broker'],
                backend=udl2_conf['celery']['backend'],
                include=udl2_conf['celery']['include'],
                loader=UDL2CeleryLoader)

celery = configure_celery(udl2_conf, celery)

if __name__ == '__main__':
    celery.start()
