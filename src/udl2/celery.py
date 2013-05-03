from __future__ import absolute_import
from celery import Celery
from kombu import Exchange, Queue


celery = Celery('udl2.celery', # where the celery system is. the name is due to convention in celery see http://docs.celeryproject.org/en/latest/getting-started/next-steps.html
                broker='amqp://guest@localhost//', # this is the url to message broker. Currently it is located on localhost for rabbitmq
                backend='amqp://guest@localhost//', # this is the url to task results for each request. Currently it is located on localhost for rabbitmq
                include=['udl2.W_file_splitter',  # python files that define tasks in worker pools.
                         'udl2.W_file_loader',
                         'udl2.W_final_cleanup'])

q_default_celery = Exchange('celery', type='direct')
q_files_to_be_split_exchange =  Exchange('Q_files_to_be_split', type='direct')
q_files_to_be_loaded_exchange =  Exchange('Q_files_to_be_loaded', type='direct')
q_final_cleanup_exchange =  Exchange('Q_final_cleanup', type='direct')

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=10, # TTL for results
    CELERYD_CONCURRENCY=10, # number of available workers processes
    CELERY_SEND_EVENTS=True, # send events for monitor
    CELERY_DEFAULT_QUEUE = 'celery',
    CELERY_DEFAULT_EXCHANGE = 'direct',
    CELERY_DEFAULT_ROUTING_KEY = 'celery',
    CELERY_QUEUES = ( 
       Queue('celery', q_default_celery, routing_key='celery'),
       Queue('Q_files_to_be_split', q_files_to_be_split_exchange, routing_key='udl2'),
       Queue('Q_files_to_be_loaded', q_files_to_be_loaded_exchange, routing_key='udl2'),
       Queue('Q_final_cleanup', q_final_cleanup_exchange, routing_key='udl2'),
    ), # Add our own queues for each task
    CELERY_ROUTES = {
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
    }
)

if __name__ == '__main__':
    celery.start()