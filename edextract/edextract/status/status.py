'''
Created on Oct 31, 2013

@author: dip
'''
from edcore.database.stats_connector import StatsDBConnection
from edextract.status.constants import Constants
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection
import json
from uuid import uuid4


class ExtractStatus():
    QUEUED = 'QUEUED'               # Extract is queued in broker
    EXTRACTING = 'EXTRACTING'       # Extracting is in progress
    EXTRACTED = 'EXTRACTED'         # File has been extracted in work zone
    COPYING = 'COPYING'             # File is being copied to pick up zone
    COPIED = 'COPIED'               # File has been copied to pick up zone
    COMPLETED = 'COMPLETED'         # Extract process is completed
    FAILED = 'FAILED'                 # Extract process failed
    NO_TENANT = 'NO_TENANT'         # Extract process failed due to no tenant given


def insert_extract_stats(values):
    '''
    Insert into extract status table

    :params dict values:  dictionary of values to insert

    ex. values = {Constants.TENANT, "tenantName", Constants.STATE_CODE, "EX"}
    '''
    with StatsDBConnection() as connector:
        extract_stats = connector.get_table(Constants.EXTRACT_STATS)
        stmt = extract_stats.insert(values=values)
        connector.execute(stmt)


def update_extract_stats(task_id, values):
    '''
    Update extract status table

    :params string task_id:  celery task id
    :params dict values:  dictionary of values to update

    ex. values = {Constants.STATE_CODE, "EX"}
    '''
    with StatsDBConnection() as connector:
        extract_stats = connector.get_table(Constants.EXTRACT_STATS)
        stmt = extract_stats.update().\
            where(extract_stats.c.task_id == task_id).\
            values(values)
        connector.execute(stmt)


def setup_db_connection(settings):
    '''
    Given ini key/value pair, initialize db for stats table
    '''
    initialize_db(EdCoreDBConnection, settings)
    initialize_db(StatsDBConnection, settings, allow_schema_create=True)


def create_new_status(user, request_id, params, status=ExtractStatus.QUEUED):
    task_id = str(uuid4())

    insert_extract_stats({Constants.REQUEST_GUID: request_id,
                          Constants.EXTRACT_PARAMS: json.dumps(params),
                          Constants.TENANT: user.get_tenant(),
                          Constants.EXTRACT_STATUS: status,
                          Constants.USER_GUID: user.get_guid(),
                          Constants.TASK_ID: task_id})
    return task_id
