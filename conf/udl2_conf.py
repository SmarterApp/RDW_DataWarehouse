#!/usr/bin/env python

udl2_conf = {
    'celery':{'root':'udl2.celery', # where the celery system is defined. the name is due to convention in celery see http://docs.celeryproject.org/en/latest/getting-started/next-steps.html
              'broker':'amqp://guest@localhost//',  # this is the url to message broker. Currently it is located on localhost for rabbitmq
              'backend':'amqp://guest@localhost//',  # this is the url to task results for each request. Currently it is located on localhost for rabbitmq
              'include':['udl2.W_file_splitter',  # python files that define tasks in worker pools.
                         'udl2.W_file_loader',
                         'udl2.W_final_cleanup'],
    },
    'file_splitter':{
        'row_limit': 10000,
        'parts': 5,
        'output_path' : '.',
        'keep_headers' : True,
    },
    'celery_defaults': {
        'CELERY_DEFAULT_QUEUE':'celery', # default celery queue name for celery internal tasks
        'CELERY_DEFAULT_EXCHANGE':'direct', # default celery exchange name, and exchange type
        'CELERY_DEFAULT_ROUTING_KEY':'celery', # default celery routing key for tasks
        'CELERY_TASK_RESULT_EXPIRES':10,  # TTL for results
        'CELERYD_CONCURRENCY':10,  # number of available workers processes
        'CELERY_SEND_EVENTS':True,  # send events for monitor
    },
    'udl2_queues':{
        'stage_1': {'name':'Q_files_to_be_split',
                    'exchange': {'name': 'Q_files_to_be_split', 'type': 'direct'},
                    'routing_key':'udl2'},
        'stage_2': {'name':'Q_files_to_be_loaded',
                    'exchange': {'name': 'Q_files_to_be_loaded', 'type': 'direct'},
                    'routing_key':'udl2'},
        'stage_3': {'name':'Q_final_cleanup',
                    'exchange': {'name': 'Q_final_cleanup', 'type': 'direct'},
                    'routing_key':'udl2'},    
    },
    'udl2_stages':{
        'stage_1':{'task_name':'udl2.W_file_splitter.task',
                   'description':'',
                   'queue_name':'Q_files_to_be_split',
                   'routing_key':'udl2',
                   'next':'stage_2',
                   'prev':None
        },
        'stage_2':{'task_name':'udl2.W_file_loader.task',
                   'description':'',
                   'queue_name':'Q_files_to_be_loaded',
                   'routing_key':'udl2',
                   'next':'stage_3',
                   'prev':'stage_1',
        },
        'stage_3':{'task_name':'udl2.W_final_cleanup.task',
                   'description':'',
                   'queue_name':'Q_files_to_be_loaded',
                   'routing_key':'udl2',
                   'next':None,
                   'prev':'stage_2',
        }
    },
    'rabbitmq': {
        'RABBITMQ_SERVER':'/opt/local/sbin/rabbitmq-server',
    },
    'postgresql' : {
        'db_host':'',
        'db_port':'',
        'db_db':'',
    }
}


if __name__ == '__main__':
    print("udl2 config file\n")
    print(udl2_conf)
