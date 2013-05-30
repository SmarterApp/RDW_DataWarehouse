#!/usr/bin/env python

udl2_conf = {
    'celery':{'root':'udl2.celery',  # where the celery system is defined. the name is due to convention in celery see http://docs.celeryproject.org/en/latest/getting-started/next-steps.html
              'broker':'amqp://guest@localhost//',  # this is the url to message broker. Currently it is located on localhost for rabbitmq
              'backend':'amqp://guest@localhost//',  # this is the url to task results for each request. Currently it is located on localhost for rabbitmq
              'include':['udl2.W_file_arrived',
                         'udl2.W_file_expander',
                         'udl2.W_simple_file_validator',
                         'udl2.W_file_splitter',
                         'udl2.W_load_csv_to_staging',
                         'udl2.W_file_content_validator',
                         'udl2.W_load_json_to_integration',
                         'udl2.W_load_to_integration_table',
                         'udl2.W_load_from_integration_to_star',
                         'udl2.W_report_error_or_success',
                         'udl2.W_final_cleanup'
              ],
    },
    'file_splitter':{  # Options for file_splitter
        'row_limit': 10000,  # default row number for split files
        'parts': 1,  # default parts of files
        'output_path' : '.',  # where the newly generated split file located
        'keep_headers' : True,  # preserve csv header for importing
    },
    'celery_defaults': {
        'CELERY_DEFAULT_QUEUE':'celery',  # default celery queue name for celery internal tasks
        'CELERY_DEFAULT_EXCHANGE':'direct',  # default celery exchange name, and exchange type
        'CELERY_DEFAULT_ROUTING_KEY':'celery',  # default celery routing key for tasks
        'CELERY_TASK_RESULT_EXPIRES':10,  # TTL for results
        'CELERY_CONCURRENCY':10,  # number of available workers processes
        'CELERY_SEND_EVENTS':True,  # send events for monitor
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
        'db_driver':'postgresql',
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
        'db_driver':'postgresql',
    },
    'target_db': {
        'db_schema': 'edware',
        # TBD, make sure it is the production setting
        'db_host':'localhost',
        'db_port':'5432',
        'db_database':'edware',
        'db_user':'edware',
        'db_pass':'password',
        'db_driver':'postgresql'
    }
}


if __name__ == '__main__':
    print("udl2 config file\n")
    print(udl2_conf)
