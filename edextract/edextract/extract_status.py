'''
Created on Oct 31, 2013

@author: dip
'''
from edcore.database.stats_connector import StatsDBConnection
from edextract.constants import Constants
from edcore.database import initialize_db


def insert_extract_stats(values):
    '''
    Insert into extract status table

    :params dict values:  dictionary of values to insert
    '''
    with StatsDBConnection() as connector:
        extract_stats = connector.get_table(Constants.EXTRACT_STATS)
        stmt = extract_stats.insert(values={extract_stats.c.state_code: values.get(Constants.STATE_CODE),
                                            extract_stats.c.tenant: values.get(Constants.TENANT),
                                            extract_stats.c.user_guid: values.get(Constants.USER_GUID),
                                            extract_stats.c.extract_status: values.get(Constants.EXTRACT_STATUS),
                                            extract_stats.c.extract_params: values.get(Constants.EXTRACT_PARAMS),
                                            extract_stats.c.task_id: values.get(Constants.TASK_ID)})
        connector.execute(stmt)


def setup_db_connection(settings):
    '''
    Given ini key/value pair, initialize db for stats table
    '''
    initialize_db(StatsDBConnection, settings, allow_schema_create=True)
