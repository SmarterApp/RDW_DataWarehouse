'''
Created on Jun 23, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import select
from smarter.trigger.database.constants import Constants
from smarter.database.udl_stats_connector import StatsDBConnection


def get_ed_stats():
    '''
    update last_pre_cached field
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(Constants.UDL_STATS)
        query = select([udl_stats.c.tenant.label(Constants.TENANT),
                        udl_stats.c.state_code.label(Constants.STATE_CODE),
                        udl_stats.c.load_start.label(Constants.LOAD_START),
                        udl_stats.c.load_end.label(Constants.LOAD_END),
                        udl_stats.c.record_loaded_count.label(Constants.RECORD_LOADED_COUNT),
                        udl_stats.c.last_pre_cached.label(Constants.LAST_PRE_CACHED), ],
                       from_obj=[udl_stats])
        query = query.where(udl_stats.c.load_status == 'ingested')
        return connector.get_result(query)
