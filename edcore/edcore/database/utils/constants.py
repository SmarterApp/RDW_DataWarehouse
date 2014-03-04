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
    TENANT = 'tenant'
    FILE_ARRIVED = 'file_arrived'
    LOAD_START = 'load_start'
    LOAD_END = 'load_end'
    LOAD_TYPE = 'load_type'
    LOAD_STATUS = 'load_status'
    RECORD_LOADED_COUNT = 'record_loaded_count'
    UDL_STATS = 'udl_stats'
    # Available Load Status
    UDL_STATUS_RECEIVED = 'udl.received'
    UDL_STATUS_FAILED = 'udl.failed'
    UDL_STATUS_LOADING = 'udl.loading'
    UDL_STATUS_INGESTED = 'udl.ingested'
