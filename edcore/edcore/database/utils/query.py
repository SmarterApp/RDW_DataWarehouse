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

from edcore.database.stats_connector import StatsDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from sqlalchemy.sql.expression import select, and_


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


def get_udl_stats_by_date(start_date, end_date=None):
    '''
    return all udl_stats records by given date
    '''
    results = []
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        s = select([udl_stats.c.tenant, udl_stats.c.file_arrived, udl_stats.c.load_start, udl_stats.c.load_end, udl_stats.c.load_status, udl_stats.c.batch_guid])
        if end_date is None:
            s = s.where(udl_stats.c.file_arrived >= start_date)
        else:
            s = s.where(and_(udl_stats.c.file_arrived >= start_date, udl_stats.c.file_arrived < end_date))
        results = connector.get_result(s)
    return results
