__author__ = 'abrien'

# LZ to file_arrived
INPUT_FILE_PATH = 'input_file_path'
LANDING_ZONE_WORK_DIR = 'landing_zone_work_dir'
GUID_BATCH = 'guid_batch'

# file_arrived to file_decrypter
FILE_TO_DECRYPT = 'file_to_decrypt'
INPUT_FILE_SIZE = 'input_file_size'
TENANT_DIRECTORY_PATHS = 'tenant_directory_paths'
ARRIVED = 'arrived'
DECRYPTED = 'decrypted'
EXPANDED = 'expanded'
SUBFILES = 'subfiles'
HISTORY = 'history'

# file_decrypter to file_expander
FILE_TO_EXPAND = 'file_to_expand'

# file_expander to file_validator
JSON_FILENAME = 'json_filename'
CSV_FILENAME = 'csv_filename'

# file_validator to file_splitter
PARTS = 'parts'

# file_splitter to csv_to_staging
FILE_TO_LOAD = 'file_to_load'
ROW_START = 'row_start'
HEADERS = 'headers'
APPLY_RULES = 'apply_rules'
LINE_COUNT = 'line_count'
SPLIT_FILE_LIST = 'split_file_tuple_list'
HEADER_FILE_PATH = 'header_file_path'

# json_to_integration
MAPPINGS = 'mappings'

# keys for conf sent to file_loader.load_file(conf)
TARGET_DB_HOST = 'target_db_host'
TARGET_DB_PORT = 'target_db_port'
TARGET_DB_USER = 'target_db_user'
TARGET_DB_NAME = 'target_db_name'
TARGET_DB_PASSWORD = 'target_db_password'
TARGET_DB_SCHEMA = 'target_db_schema'
TARGET_DB_TABLE = 'target_db_table'
CSV_SCHEMA = 'csv_schema'
CSV_TABLE = 'csv_table'
FDW_SERVER = 'fdw_server'
REF_TABLE = 'ref_table'
CSV_LZ_TABLE = 'csv_lz_table'
ERR_LIST_TABLE = 'err_list_table'

# keys for conf sent to move_to_integration.move_data_from_staging_to_integration(conf)
SOURCE_DB_DRIVER = 'source_db_driver'
SOURCE_DB_USER = 'source_db_user'
SOURCE_DB_PASSWORD = 'source_db_password'
SOURCE_DB_HOST = 'source_db_host'
SOURCE_DB_PORT = 'source_db_port'
SOURCE_DB_NAME = 'source_db_name'
SOURCE_DB_SCHEMA = 'source_db_schema'
SOURCE_DB_TABLE = 'source_db_table'
ERROR_DB_SCHEMA = 'error_schema'

# keys for conf sent to move_to_integration.move_data_from_staging_to_integration(conf) for matchers
PROD_DB_HOST = 'prod_db_host'
PROD_DB_PORT = 'prod_db_port'
PROD_DB_USER = 'prod_db_user'
PROD_DB_NAME = 'prod_db_name'
PROD_DB_PASSWORD = 'prod_db_password'
PROD_DB_SCHEMA = 'prod_db_schema'
PROD_DB_TABLE = 'prod_db_table'

MAP_TYPE = 'map_type'

PHASE = 'phase'

# report errors
EMAIL = 'email_address'

# load_to_integration
INT_TABLE_TYPE = 'load_to_integration_table_type'

# move to target
MOVE_TO_TARGET = 'move_to_target'
TENANT_NAME = 'tenant_name'

TOTAL_ROWS_LOADED = 'total_rows_loaded'

# for benchmarking
UDL_PHASE = 'udl_phase'
UDL_LEAF = 'udl_leaf'
SIZE_RECORDS = 'size_records'
SIZE_UNITS = 'size_units'
TASK_ID = 'task_id'
LOAD_TYPE = 'load_type'
WORKING_SCHEMA = 'working_schema'
START_TIMESTAMP = 'start_timestamp'
END_TIMESTAMP = 'end_timestamp'
DURATION = 'duration'
UDL_PHASE_STEP = 'udl_phase_step'
UDL_PHASE_STEP_STATUS = 'udl_phase_step_status'
PIPELINE_STATE = 'pipeline_state'
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
RECORDS_PER_HOUR = 'records_per_hour'
TIME_FOR_ONE_MILLION_RECORDS = 'time_for_one_million_records'
BATCH_TABLE = 'batch_table'
USER_EMAIL = 'user_email'
TASK_URL = 'task_status_url'
TASK_URL = 'task_status_url'

# serializing pipeline
LOOP_PIPELINE = 'loop_pipeline'
TENANT_SEARCH_PATHS = 'tenant_search_paths'

# notification
STUDENT_REG_GUID = 'student_reg_guid'
REG_SYSTEM_ID = 'reg_system_id'
CALLBACK_URL = 'callback_url'
