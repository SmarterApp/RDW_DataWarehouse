'''
Created on Jul 29, 2014

@author: tosako
'''
from edworker.celery import setup_celery as setup_for_worker, configure_celeryd,\
    get_config_file
from smarter_score_batcher.trigger.file_monitor import run_cron_sync_file


PREFIX = 'smarter_score_batcher.celery'


def setup_celery(settings, prefix=PREFIX):
    '''
    Setup celery based on parameters defined in setting (ini file).
    This calls by client application when dictionary of settings is given

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    global conf
    conf = settings
    setup_for_worker(celery, settings, prefix)
    run_cron_sync_file(settings)


# Create an instance of celery, check if it's for prod celeryd mode and configure it for prod mode if so
celery, conf = configure_celeryd(PREFIX, prefix=PREFIX)
prod_config = get_config_file()
if prod_config:
    setup_celery(conf)
