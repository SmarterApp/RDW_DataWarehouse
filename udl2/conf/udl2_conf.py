#!/usr/bin/env python

udl2_conf = {
    'celery': {'root': 'udl2.celery',  # where the celery system is defined. the name is due to convention in celery see http://docs.celeryproject.org/en/latest/getting-started/next-steps.html
               'broker': 'amqp://guest@localhost//',  # this is the url to message broker. Currently it is located on localhost for rabbitmq
               'backend': 'amqp://guest@localhost//',  # this is the url to task results for each request. Currently it is located on localhost for rabbitmq
               'include': ['udl2.W_file_arrived',
                           'udl2.W_file_decrypter',
                           'udl2.W_file_expander',
                           'udl2.W_simple_file_validator',
                           'udl2.W_file_splitter',
                           'udl2.W_parallel_csv_load',
                           'udl2.W_load_csv_to_staging',
                           'udl2.W_file_content_validator',
                           'udl2.W_load_json_to_integration',
                           'udl2.W_load_to_integration_table',
                           'udl2.W_load_from_integration_to_star',
                           'udl2.W_post_etl',
                           'udl2.W_report_error_or_success',
                           'udl2.W_all_done',
                           'benchmarking.run_benchmarks',
                           ],
               },
    'file_splitter': {  # Options for file_splitter
        'row_limit': 10000,  # default row number for split files
        'parts': 1,  # default parts of files
        'output_path': '.',  # where the newly generated split file located
        'keep_headers': True,  # preserve csv header for importing
    },
    'move_to_target': [{'rec_id': 'asmt_rec_id',
                        'target_table': 'dim_asmt',
                        'source_table': 'INT_SBAC_ASMT',
                        'guid_column_name': 'asmt_guid',
                        'guid_column_in_source': 'guid_asmt'},

                       {'rec_id_map': ('inst_hier_rec_id', 'inst_hier_rec_id'),
                        'table_map': ('dim_inst_hier', 'fact_asmt_outcome'),
                        'guid_column_map': dict([('state_code', 'state_code'),
                                                 ('district_guid', 'district_guid'),
                                                 ('school_guid', 'school_guid')])},
                       {'rec_id': 'section_rec_id',
                        'value': '1'}
                       ],
    'celery_defaults': {
        'CELERY_DEFAULT_QUEUE': 'celery',  # default celery queue name for celery internal tasks
        'CELERY_DEFAULT_EXCHANGE': 'direct',  # default celery exchange name, and exchange type
        'CELERY_DEFAULT_ROUTING_KEY': 'celery',  # default celery routing key for tasks
        'CELERY_TASK_RESULT_EXPIRES': 10,  # TTL for results
        'CELERY_CONCURRENCY': 10,  # number of available workers processes
        'CELERY_SEND_EVENTS': True,  # send events for monitor
    },
    'rabbitmq': {  # rabbitmq server for local testing if we requires to bring up a rabbitmq server for UDL2 celery tasks on this machine. It will be ignore by celery if there are global rabbitmq-server
        'RABBITMQ_SERVER_PATH': ['/opt/local/sbin/rabbitmq-server', '/usr/local/sbin/rabbitmq-server'],  # where the rabbitmq-server is located, we list all possible locations in your system.
    },
    'zones': {  # zones for where the files are uploaded and processed. it may change to other mechanisms, but we uses local file system for the moment.
        'landing': '/opt/wgen/edware-udl/zones/landing/',  # this is for where the uploaded files are located, it may be an url in the long run to get data
        'arrivals': '/opt/wgen/edware-udl/zones/landing/arrivals/',  # this is where the file arrives.
        'work': '/opt/wgen/edware-udl/zones/landing/work/',  # this is the where the file are use for work. this should always be local for speed
        'history': '/opt/wgen/edware-udl/zones/landing/history/',  # this is where we store historical info. it may be an url for large file storages such as s3.
        'pickup': '/opt/wgen/edware-udl/zones/pickup/',  # pickup zone where we store outgoing files
        'pickup-work': '/opt/wgen/edware-udl/zones/pickup/work',
        'pickup-departures': '/opt/wgen/edware-udl/zones/pickup/departures',
        'pickup-history': '/opt/wgen/edware-udl/zones/pickup/history',
        'datafiles': '/opt/wgen/edware-udl/zones/datafiles/',  # this is for storing test sample data files
        'tests': '/opt/wgen/edware-udl/zones/tests/',  # this is for running unit tests.
    },
    'work_zone_sub_dir': {
        'arrived': 'arrived',
        'decrypted': 'decrypted',
        'expanded': 'expanded',
        'subfiles': 'subfiles',
        'history': 'history'
    },
    'logging': {  # log location. this should be in the long run as file locations or more sophisticated logging system
        'level': 'INFO',
        'debug': 'FALSE',
        'audit': '/var/log/wgen/edware-udl/logs/udl2.audit.log',  # for status log for everything
        'error': '/var/log/wgen/edware-udl/logs/udl2.error.log',  # for error message and exceptions,
    },
    'multi_tenant': {
        'on': False,
        'default_tenant': 'edware',
    },
    'udl2_db': {
        'csv_schema': 'udl2',  # PostgresQL for UDL2 processing. This is not the target database.
        'reference_schema': 'udl2',
        'fdw_server': 'udl2_fdw_server',
        'staging_schema': 'udl2',
        'integration_schema': 'udl2',
        'ref_table_name': 'REF_COLUMN_MAPPING',
        'batch_table': 'UDL_BATCH',
        'db_host': 'localhost',
        'db_port': '5432',
        'db_name': 'udl2',
        'db_database': 'udl2',
        'db_schema': 'udl2',
        'db_user': 'udl2',
        'db_pass': 'udl2abc1234',
        'db_driver': 'postgresql',
        'json_lz_table': 'LZ_JSON',
        'csv_lz_table': 'LZ_CSV',
        'master_metadata_table': 'MASTER_METADATA',
        # sqlalchemy specific
        'echo': False,
        'max_overflow': 10,
        'pool_size': 20,
    },
    'udl2_db_conn': {
        'url': 'postgresql://udl2:udl2abc1234@localhost:5432/udl2',
        'db_schema': 'udl2',
        'echo': False,
        'max_overflow': 10,
        'pool_size': 20,
    },
    'target_db_conn': {
        'edware': {
            'url': 'postgresql://edware:edware2013@localhost:5432/edware',
            'db_schema': 'edware',
            'echo': False,
            'max_overflow': 10,
            'pool_size': 20,
            'db_database': 'edware',
            'db_user': 'edware',
            'db_pass': 'edware2013',
        },
        'CA': {
            'url': 'postgresql://edware:edware2013@localhost:5432/edware',
            'db_schema': 'edware',
            'echo': False,
            'max_overflow': 10,
            'pool_size': 20,
            'db_database': 'edware',
            'db_user': 'edware',
            'db_pass': 'edware2013',
        },
        'func_tests': {
            'url': 'postgresql://edware:edware2013@localhost:5432/edware',
            'db_schema': 'ftest_test_schema',
            'echo': False,
            'max_overflow': 10,
            'pool_size': 20,
            'db_database': 'edware',
            'db_user': 'edware',
            'db_pass': 'edware2013',
        },
        'func_tests_b': {
            'url': 'postgresql://edware:edware20133@localhostblah:5432/edware',
            'db_schema': 'ftest_test_schema',
            'echo': False,
            'max_overflow': 10,
            'pool_size': 20,
            'db_database': 'edware',
            'db_user': 'edware',
            'db_pass': 'edware2013',
        }
    },
    'target_db': {
        'db_schema': 'edware',
        'db_name': 'edware',
        # TBD, make sure it is the production setting
        'db_host': 'localhost',
        'db_port': '5432',
        'db_database': 'edware',
        'db_user': 'edware',
        'db_pass': 'edware2013',
        'db_driver': 'postgresql'
    },
    'quiet_mode': False,
    'gpg_home': '/opt/wgen/edware-udl/zones/datafiles/keys',
    'passphrase': 'sbac udl2',
    'tenant_position': -4,
    'search_wait_time': 10,
}


if __name__ == '__main__':
    print("udl2 config file\n")
    print(udl2_conf)
