'''
Created on Oct 31, 2013

@author: dip
'''
from edcore.database.stats_connector import StatsDBConnection
from edextract.constants import Constants
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection


class ExtractStatus():
    QUEUED = 'QUEUED'               # Extract is queued in broker
    STARTED = 'STARTED'             # Celery Worker has dequeued the task
    EXTRACTING = 'EXTRACTING'       # Extracting is in progress
    EXTRACTED = 'EXTRACTED'         # File has been extracted in work zone
    COPYING = 'COPYING'             # File is being copied to pick up zone
    COPIED = 'COPIED'               # File has been copied to pick up zone
    COMPLETED = 'COMPLETED'         # Extract process is completed


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
