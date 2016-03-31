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
Created on Dec 9, 2013

@author: dip
'''

import pkg_resources


class ExtractionDataType():
    SR_STATISTICS = 'StudentRegistrationStatisticsReportCSV'
    SR_COMPLETION = 'StudentAssessmentCompletionReportCSV'
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
    THRESHOLD_SIZE = 'threshold_size'
    TEMPLATE_DIR = pkg_resources.resource_filename('edextract', 'templates')


class QueryType():
    QUERY = 'query'
    MATCH_ID_QUERY = 'match_id_query'
    ASMT_OUTCOME_QUERY = 'asmt_outcome_query'
