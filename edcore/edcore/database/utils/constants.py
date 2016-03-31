# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Mar 1, 2014

@author: dip
'''


class UdlStatsConstants():
    '''
    Constants related to extracts
    '''
    REC_ID = 'rec_id'
    BATCH_GUID = 'batch_guid'
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
    BATCH_OPERATION = 'batch_operation'
    SNAPSHOT_CRITERIA = 'snapshot_criteria'
    NOTIFICATION = 'notification'
    NOTIFICATION_STATUS = 'notification_status'
    # Available Load Status
    UDL_STATUS_RECEIVED = 'udl.received'
    UDL_STATUS_FAILED = 'udl.failed'
    UDL_STATUS_LOADING = 'udl.loading'
    UDL_STATUS_INGESTED = 'udl.ingested'
    MIGRATE_IN_PROCESS = 'migrate.in_process'
    MIGRATE_INGESTED = 'migrate.ingested'
    MIGRATE_FAILED = 'migrate.failed'
    # Available Batch Operations
    SNAPSHOT = 's'


class LoadType():
    ASSESSMENT = 'assessment'
    STUDENT_REGISTRATION = 'studentregistration'


class AssessmentType():
    SUMMATIVE = 'SUMMATIVE'
    INTERIM_COMPREHENSIVE = 'INTERIM COMPREHENSIVE'
    INTERIM_ASSESSMENTS_BLOCKS = 'INTERIM ASSESSMENT BLOCKS'


class Constants():
    STATUS_CURRENT = 'C'
    STATUS_SHADOW = 'S'
    STATUS_DELETE = 'D'
    STATUS_WAITING = 'W'
    BATCH_GUID = 'batch_guid'
    GUID_BATCH = 'guid_batch'
    REC_STATUS = 'rec_status'
    DIM_TABLES_PREFIX = 'dim_'
    FACT_TABLES_PREFIX = 'fact_'
    META_COLUMN = 'MetaColumn'
    RECORD_SID = 'record_sid'
