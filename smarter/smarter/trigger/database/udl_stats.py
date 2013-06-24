'''
Created on Jun 23, 2013

@author: tosako
'''
from smarter.trigger.database.connector import StatsDBConnection
from sqlalchemy.sql.expression import select

def get_ed_stats():
    '''
    update last_pre_cached field
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table('udl_stats')
        query = select([udl_stats.c.tenant.label('tenant'),
                        udl_stats.c.state_code.label('state_code'),
                        udl_stats.c.load_start.label('load_start'),
                        udl_stats.c.load_end.label('load_end'),
                        udl_stats.c.record_loaded_count.label('record_loaded_count'),
                        udl_stats.c.last_pre_cached.label('last_pre_cached'), ],
                       from_obj=[udl_stats])
        query = query.where(udl_stats.c.load_status == 'ingested')
        return connector.get_result(query)
