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
from datetime import datetime
from edcore.utils.utils import merge_dict


class ExtractStatus():
    QUEUED = 'QUEUED'                       # Extract is queued in broker
    EXTRACTING = 'EXTRACTING'               # Extracting is in progress
    EXTRACTED = 'EXTRACTED'                 # File has been extracted in work zone
    GENERATING_JSON = 'GENERATING_JSON'     # Generating json
    GENERATED_JSON = 'GENERATED_JSON'       # Generated json and file is saved to disk
    ARCHIVING = 'ARCHIVING'                 # File is being archived
    ARCHIVED = 'ARCHIVED'                   # File is archived
    COPYING = 'COPYING'                     # File is being copied to pick up zone
    COPIED = 'COPIED'                       # File has been copied and entire extract process is completed
    # Error status
    FAILED = 'FAILED'                       # Extract process failed
    FAILED_NO_TENANT = 'FAILED_NO_TENANT'   # Extract process failed due to no tenant given


def insert_extract_stats(*dict_values):
    '''
    Insert into extract status table

    :params dict values:  one or more dictionary of values to insert

    ex. dict_values = {Constants.TENANT, "tenantName": Constants.STATE_CODE: "EX"}, {Constants.OTHER: "test"}
    '''
    values = {Constants.TIMESTAMP: datetime.utcnow()}
    for d in dict_values:
        values = merge_dict(d, values)

    with StatsDBConnection() as connector:
        extract_stats = connector.get_table(Constants.EXTRACT_STATS)
        stmt = extract_stats.insert(values)
        connector.execute(stmt)


def delete_stats():
    '''
    Deletes table
    '''
    with StatsDBConnection() as connector:
        extract_stats = connector.get_table(Constants.EXTRACT_STATS)
        connector.execute(extract_stats.delete())


def setup_db_connection(settings):
    '''
    Given ini key/value pair, initialize db for stats table
    '''
    initialize_db(EdCoreDBConnection, settings)
    initialize_db(StatsDBConnection, settings, allow_schema_create=True)


def create_new_entry(user, request_id, params, status=ExtractStatus.QUEUED):
    task_id = str(uuid4())

    insert_extract_stats({Constants.REQUEST_GUID: request_id,
                          Constants.INFO: json.dumps({'params': params, 'tenant': user.get_tenants(), 'user_guid': user.get_guid()}),
                          Constants.STATUS: status,
                          Constants.TASK_ID: task_id})
    return task_id
