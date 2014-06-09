__author__ = 'sravi'

"""
Utility methods for CSV and JSON validators
"""

from sqlalchemy.sql import select
from edudl2.udl2.constants import Constants
from edudl2.database.udl2_connector import get_udl_connection


def get_source_column_values_from_ref_column_mapping(source_table, load_type):
    """
    return all data for source_column from ref_column_mapping based on source_table value passed
    :param: source_table: source_table values to query for
    :return: A set containing all the columns expected in a source csv file
    """
    with get_udl_connection() as conn:
        table_meta = conn.get_table(Constants.UDL2_REF_MAPPING_TABLE(load_type))
        select_object = select([table_meta]).where(table_meta.c.source_table == source_table)
        return [row['source_column'] for row in conn.execute(select_object)]


def get_source_target_column_values_from_ref_column_mapping(source_table, load_type):
    """
    return all data for source_column from ref_column_mapping based on source_table value passed
    :param: source_table: source_table values to query for
    :return: A set containing all the columns expected in a source csv file
    """
    with get_udl_connection() as conn:
        table_meta = conn.get_table(Constants.UDL2_REF_MAPPING_TABLE(load_type))
        select_object = select([table_meta]).where(table_meta.c.source_table == source_table)
        return [(row['target_column'], row['source_column']) for row in conn.execute(select_object)]
