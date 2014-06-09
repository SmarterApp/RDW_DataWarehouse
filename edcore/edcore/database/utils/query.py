from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants


def insert_to_table(conn, table_name, values):
    '''
    Generic Insertion of values into table based on a connection
    '''
    with conn() as connector:
        table = connector.get_table(table_name)
        stmt = table.insert(values)
        return connector.execute(stmt)


def update_records_in_table(conn, table_name, values, criteria):
    '''
    Updates record in table with where clause derived from criteria
    '''
    with conn() as connector:
        table = connector.get_table(table_name)
        stmt = table.update().values(values)
        for k, v in criteria.items():
            stmt = stmt.where(table.c[k] == v)
        connector.execute(stmt)


def insert_udl_stats(values):
    '''
    Insert into udl stats table
    '''
    return insert_to_table(StatsDBConnection, UdlStatsConstants.UDL_STATS, values)


def update_udl_stats(rec_id, values):
    '''
    Update udl stats table by rec_id
    '''
    update_records_in_table(StatsDBConnection, UdlStatsConstants.UDL_STATS, values,
                            {UdlStatsConstants.REC_ID: rec_id})


def update_udl_stats_by_batch_guid(batch_guid, values):
    '''
    Update udl stats table by batch_guid
    '''
    update_records_in_table(StatsDBConnection, UdlStatsConstants.UDL_STATS, values,
                            {UdlStatsConstants.BATCH_GUID: batch_guid})
