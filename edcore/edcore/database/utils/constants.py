'''
Created on Mar 1, 2014

@author: dip
'''


class UdlStatsConstants():
    '''
    Constants related to extracts
    '''
    BATCH_GUID = 'batch_guid'
    STATE_CODE = 'state_code'
    SCHEMA_NAME = 'schema_name'
    TENANT = 'tenant'
    FILE_ARRIVED = 'file_arrived'
    LOAD_START = 'load_start'
    LOAD_END = 'load_end'
    LOAD_TYPE = 'load_type'
    LOAD_STATUS = 'load_status'
    RECORD_LOADED_COUNT = 'record_loaded_count'
    LAST_PRE_CACHED = 'last_pre_cached'
    LAST_PDF_TASK_REQUESTED = 'last_pdf_task_requested'
    UDL_STATS = 'udl_stats'
    # Available Load Status
    UDL_STATUS_RECEIVED = 'udl.received'
    UDL_STATUS_FAILED = 'udl.failed'
    UDL_STATUS_LOADING = 'udl.loading'
    UDL_STATUS_INGESTED = 'udl.ingested'
    MIGRATE_IN_PROCESS = 'migrate.in_process'
    MIGRATE_INGESTED = 'migrate.ingested'
    MIGRATE_FAILED = 'migrate.failed'


class LoadType():
    ASSESSMENT = 'assessment'
    STUDENT_REGISTRATION = 'studentregistration'


class Constants():
    STATUS_CURRENT = 'C'
    STATUS_SHADOW = 'S'
    STATUS_DELETE = 'D'
    BATCH_GUID = 'batch_guid'
    REC_STATUS = 'rec_status'
    DIM_TABLES_PREFIX = 'dim_'
    FACT_TABLES_PREFIX = 'fact_'
    META_COLUMN = 'MetaColumn'
