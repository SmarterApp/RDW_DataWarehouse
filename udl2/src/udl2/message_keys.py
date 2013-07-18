from udl2_util.measurement import measure_cpu_plus_elasped_time

__author__ = 'abrien'

# LZ to file_arrived
INPUT_FILE_PATH = 'input_file_path'
JOB_CONTROL = 'job_control'
LANDING_ZONE_WORK_DIR = 'landing_zone_work_dir'
GUID_BATCH = 'guid_batch'

# file_arrived to file_expander
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

MAP_TYPE = 'map_type'

PHASE = 'phase'

# report errors
EMAIL = 'email_address'

# load_to_integration
INT_TABLE_TYPE = 'load_to_integration_table_type'
