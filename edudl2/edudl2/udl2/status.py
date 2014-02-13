from edudl2.udl2.Constants import UdlStatsConstants
__author__ = 'sravi'
from edcore.database.stats_connector import StatsDBConnection
from edcore.utils.utils import merge_dict


def insert_udl_daily_stats(*dict_values):
    '''
    Insert into udl daily stats table

    :params dict values:  one or more dictionary of values to insert

    ex. dict_values = {Constants.TENANT, "tenantName": Constants.STATE_CODE: "EX"}, {Constants.OTHER: "test"}
    '''
    values = {}
    for d in dict_values:
        values = merge_dict(d, values)

    with StatsDBConnection() as connector:
        udl_daily_stats = connector.get_table(UdlStatsConstants.UDL_DAILY_STATS)
        stmt = udl_daily_stats.insert(values)
        connector.execute(stmt)


def delete_stats():
    '''
    Deletes table
    '''
    with StatsDBConnection() as connector:
        udl_daily_stats = connector.get_table(UdlStatsConstants.UDL_DAILY_STATS)
        connector.execute(udl_daily_stats.delete())
