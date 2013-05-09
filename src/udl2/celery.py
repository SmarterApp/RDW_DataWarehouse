from __future__ import absolute_import
from celery import Celery
from kombu import Exchange, Queue
import sys

def parse_args():
    args = {}
    return args


def get_config_file(args):
    if args['config'] is None:
        return DEFAULT_CONFIG_PATH
    else:
        return args['config']
    
    
def setup_udl2_queues(conf):
    print(conf)
    queues = {}
    # set up default queues, which is always celery
    queues['default'] = Queue('celery',
                              Exchange(conf['celery_defaults']['CELERY_DEFAULT_EXCHANGE'],
                                       conf['celery_defaults']['CELERY_DEFAULT_EXCHANGE']),
                             routing_key=conf['celery_defaults']['CELERY_DEFAULT_ROUTING_KEY'])
    # set up all celery queues for UDL2
    print(conf['udl2_queues'])
    for k, v in conf['udl2_queues'].items():
        queues[k] = Queue(v['name'],
                          Exchange(v['exchange']['name'],
                                   v['exchange']['type']),
                          routing_key=v['routing_key'])
    
    return queues


def setup_udl2_stages(conf, udl2_queues):
    stages = conf['udl2_stages']
    # now we need to add connect real queue object in python
    # and real celery task with stages
    for k, v in stages.items():
        #exec("stages[k]['task'] = " + v['task_name'])
        stages[k]['queue'] =  udl2_queues[k]
    return stages


def setup_celery_conf(udl2_conf, celery, udl_queues, udl_stages):
    celery.conf.update(CELERY_TASK_RESULT_EXPIRES=10,  # TTL for results
        CELERYD_CONCURRENCY=10,  # number of available workers processes
        CELERY_SEND_EVENTS=True,  # send events for monitor
        CELERY_DEFAULT_QUEUE='celery',
        CELERY_DEFAULT_EXCHANGE='direct',
        CELERY_DEFAULT_ROUTING_KEY='celery',
        CELERY_QUEUES=tuple(udl_queues.values()),  # Add our own queues for each task
        CELERY_ROUTES={
            'udl2.W_file_splitter.task' : {
                'queue' : 'Q_files_to_be_split',
                'routing_key': 'udl2',
            },
            'udl2.W_file_loader.task' : {
                'queue' : 'Q_files_to_be_loaded',
                'routing_key' : 'udl2',
            },
            'udl2.W_final_cleanup' : {
                'queue' : 'Q_final_cleanup',
                'routing_key' : 'udl2',
            }
        })
    return celery

DEFAULT_CONFIG_PATH='/opt/wgen/edware-udl/etc/'



sys.path.append(DEFAULT_CONFIG_PATH)
from udl2_conf import udl2_conf

celery = Celery(udl2_conf['celery']['root'],  
                broker=udl2_conf['celery']['broker'], 
                backend=udl2_conf['celery']['backend'], 
                include=udl2_conf['celery']['include'])

# Create all queues entities to be use by task functions

udl2_queues = setup_udl2_queues(udl2_conf)

#print(udl2_queues)

# Create all stage entities to be use by task functions
udl2_stages = setup_udl2_stages(udl2_conf, udl2_queues)
#print(udl2_stages)


celery = setup_celery_conf(udl2_conf, celery, udl2_queues, udl2_stages)

# configuration options for file splitter
FILE_SPLITTER_CONF = udl2_conf['file_splitter']


if __name__ == '__main__':
    celery.start()
