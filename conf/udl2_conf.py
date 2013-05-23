#!/usr/bin/env python

udl2_conf = {
    'celery':{'root':'udl2.celery',  # where the celery system is defined. the name is due to convention in celery see http://docs.celeryproject.org/en/latest/getting-started/next-steps.html
              'broker':'amqp://guest@localhost//',  # this is the url to message broker. Currently it is located on localhost for rabbitmq
              'backend':'amqp://guest@localhost//',  # this is the url to task results for each request. Currently it is located on localhost for rabbitmq
              'include':['udl2.W_file_splitter',  # python files that define tasks in worker pools.
                         'udl2.W_file_loader',
                         'udl2.W_final_cleanup',
                         'udl2.W_dummy_task',
                         'udl2.W_move_to_target',
                         'udl2.W_load_to_integration_table',
                         'udl2.W_load_json_to_integration'],
    },
    'file_splitter':{  # Options for file_splitter
        'row_limit': 10000,  # default row number for split files
        'parts': 1,  # default parts of files
        'output_path' : '.',  # where the newly generated splited file located
        'keep_headers' : True,  # preserve csv header for importing
    },
    'celery_defaults': {
        'CELERY_DEFAULT_QUEUE':'celery',  # default celery queue name for celery internal tasks
        'CELERY_DEFAULT_EXCHANGE':'direct',  # default celery exchange name, and exchange type
        'CELERY_DEFAULT_ROUTING_KEY':'celery',  # default celery routing key for tasks
        'CELERY_TASK_RESULT_EXPIRES':10,  # TTL for results
        'CELERYD_CONCURRENCY':10,  # number of available workers processes
        'CELERY_SEND_EVENTS':True,  # send events for monitor
    },
    'udl2_queues':{
#        'stage_0': {'name':'Q_files_received',  # the first queue that receive input from client
#                     'exchange': {'name':'Q_files_received', 'type':'direct'},
#                    'routing_key':'udl2'
#                    },
        'stage_1': {'name':'Q_files_to_be_split',  # queue for the task that splits files for loading speed
                    'exchange': {'name': 'Q_files_to_be_split', 'type': 'direct'},
                    'routing_key':'udl2'},
        'stage_2': {'name':'Q_files_to_be_loaded',  # queue for the task that loads table from foreign data wrapper into staging table
                    'exchange': {'name': 'Q_files_to_be_loaded', 'type': 'direct'},
                    'routing_key':'udl2'},
        'stage_3': {'name':'Q_copy_to_integration', 
                    'exchange': {'name': 'Q_copy_to_integration', 'type': 'direct'},
                    'routing_key':'udl2'},
        'stage_4': {'name':'Q_copy_to_target',
                    'exchange': {'name': 'Q_copy_to_target', 'type': 'direct'},
                    'routing_key':'udl2'},
        'stage_n': {'name':'Q_final_cleanup',  # queue for accept final states of UDL job
                    'exchange': {'name': 'Q_final_cleanup', 'type': 'direct'},
                    'routing_key':'udl2'},
    },
    'udl2_stages':{
        'stage_1':{'task_name':'udl2.W_file_splitter.task',  # first task in current piple line. 
                   'description':'',  # programmers have to specify what is the celery task that will be execute in this stage
                   'queue_name':'Q_files_to_be_split',  # And the where the messages come from 
                   'routing_key':'udl2',  # And routing key, currently for all udl2 pipeline will be udl2 to differentiate it from celery's task
                   'next':'stage_2',  # We use next to specify what is the next stage id to be send to, None for termination. 
                   'prev':None,  # We use prev to specify what is the previous stage. this also helps possibly configurable message parser.
        },
        'stage_2':{'task_name':'udl2.W_file_loader.task',  # second task in current piple line. 
                   'description':'',  # programmers have to specify what is the celery task that will be execute in this stage
                   'queue_name':'Q_files_to_be_loaded',  # And the where the messages come from 
                   'routing_key':'udl2',  # And routing key, currently for all udl2 pipeline will be udl2 to differentiate it from celery's task
                   'next':'stage_3',  # We use next to specify what is the next stage id to be send to, None for termination. 
                   'prev':'stage_1',  # We use prev to specify what is the previous stage. this also helps possibly configurable message parser.
        },
        'stage_3':{'task_name':'udl2.W_load_to_integration_table.task',  # thrid task in current piple line. 
                   'description':'',  # programmers have to specify what is the celery task that will be execute in this stage
                   'queue_name':'Q_copy_to_integration',  # And the where the messages come from 
                   'routing_key':'udl2',  # And routing key, currently for all udl2 pipeline will be udl2 to differentiate it from celery's task
                   'next':'stage_4',  # We use next to specify what is the next stage id to be send to, None for termination.
                   'prev':'stage_2',  # We use prev to specify what is the previous stage. this also helps possibly configurable message parser.
        },
        'stage_4':{'task_name':'udl2.W_move_to_target.task',  # fourth task in current piple line. 
                   'description':'',  # programmers have to specify what is the celery task that will be execute in this stage
                   'queue_name':'Q_copy_to_target',  # And the where the messages come from 
                   'routing_key':'udl2',  # And routing key, currently for all udl2 pipeline will be udl2 to differentiate it from celery's task
                   'next':'stage_n',  # We use next to specify what is the next stage id to be send to, None for termination.
                   'prev':'stage_3',  # We use prev to specify what is the previous stage. this also helps possibly configurable message parser.
        },
        'stage_n':{'task_name':'udl2.W_final_cleanup.task',  # final task in current piple line. 
                   'description':'',  # programmers have to specify what is the celery task that will be execute in this stage
                   'queue_name':'Q_files_to_be_loaded',  # And the where the messages come from 
                   'routing_key':'udl2',  # And routing key, currently for all udl2 pipeline will be udl2 to differentiate it from celery's task
                   'next':None,  # We use next to specify what is the next stage id to be send to, None for termination.
                   'prev':'stage_4',  # We use prev to specify what is the previous stage. this also helps possibly configurable message parser.
        },
    },
    'rabbitmq': {  # rabbitmq server for local testing if we requires to bring up a rabbitmq server for UDL2 celery tasks on this machine. It will be ignore by celery if there are global rabbitmq-server
        'RABBITMQ_SERVER_PATH':'/opt/local/sbin/rabbitmq-server',  # where the rabbitmq-server is located
    },
    'zones': {  # zones for where the files are uploaded and processed. it may change to other mechanisms, but we uses local file system for the moment.
        'landing':'/opt/wgen/edware-udl/zones/landing/',  # this is for where the uploaded files are located, it may be an url in the long run to get data
        'work':'/opt/wgen/edware-udl/zones/work/',  # this is the where the file are use for work. this should always be local for speed
        'history':'/opt/wgen/edware-udl/zones/history/',  # this is where we store historical info. it may be an url for large file storages such as s3.
        'datafiles':'/opt/wgen/edwared-udl/zones/datafiles/',  # this is for storing test sample data files
    },
    'logging': {  # log location. this should be in the long run as file locations or more sophisticated logging system
        'audit':'/var/log/wgen/edware-udl/logs/udl2.audit.log',  # for status log for everything
        'error':'/var/log/wgen/edware-udl/logs/udl2.error.log',  # for error message and exceptions, 
    },
    'postgresql' : {  # PostgresQL for UDL2 processing. This is not the target database.
        'db_host':'localhost',
        'db_port':'5432',
        'db_database':'udl2',
        'db_schema':'udl2',
        'db_user':'udl2',
        'db_pass':'udl2abc1234',
        'db_driver':'postgres',
    },
    'udl2_db': {
        'csv_schema':'udl2',  # this is the same as postgresql schema
        'fdw_server':'udl2_fdw_server',
        'staging_schema':'udl2',
        'integration_schema': 'udl2',
        'db_host':'localhost',
        'db_port':'5432',
        'db_name':'udl2',
        'db_database':'udl2',
        'db_schema':'udl2',
        'db_user':'udl2',
        'db_pass':'udl2abc1234',
        'db_driver':'postgres',
    },
    'target_db': {
        'db_schema': 'edware',
        # TBD, make sure it is the production setting
        'db_host':'localhost',
        'db_port':'5432',
        'db_database':'edware',
        'db_user':'edware',
        'db_pass':'password',
        'db_driver':'postgres'
    }
}


if __name__ == '__main__':
    print("udl2 config file\n")
    print(udl2_conf)
