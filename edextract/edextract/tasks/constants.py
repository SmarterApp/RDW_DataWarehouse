'''
Created on Dec 9, 2013

@author: dip
'''


class ExtractionDataType():
    SR_STATISTICS = 'StudentRegistrationStatisticsReportCSV'
    SR_COMPLETION = 'StudentRegistrationCompletionReportCSV'
    QUERY_CSV = 'QueryCSVExtract'
    QUERY_JSON = 'QueryJSONExtract'
    QUERY_ITEMS_CSV = 'QueryItemsCSVExtract'
    QUERY_RAW_XML = 'QueryRawXML'


class Constants():
    TASK_IS_JSON_REQUEST = 'is_json_request'
    TASK_TASK_ID = 'task_id'
    CELERY_TASK_ID = 'celery_task_id'
    TASK_FILE_NAME = 'file_name'
    TASK_QUERIES = 'task_queries'
    CSV_HEADERS = 'csv_headers'
    DEFAULT_QUEUE_NAME = 'extract'
    SYNC_QUEUE_NAME = 'extract_sync'
    ARCHIVE_QUEUE_NAME = 'extract_archve'
    TENANT = 'tenant'
    STATE_CODE = 'state_code'
    ACADEMIC_YEAR = 'academicYear'
    EXTRACTION_DATA_TYPE = 'extraction_data_type'
    ROOT_DIRECTORY = 'root_directory'
    ITEM_IDS = 'item_ids'
    DIRECTORY_TO_ARCHIVE = 'directory_to_archive'


class QueryType():
    QUERY = 'query'
    MATCH_ID_QUERY = 'match_id_query'
    ASMT_OUTCOME_QUERY = 'asmt_outcome_query'
