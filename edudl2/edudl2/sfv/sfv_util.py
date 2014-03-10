__author__ = 'sravi'

"""
Utility methods for CSV and JSON validators
"""

from sqlalchemy.sql import select
from edudl2.udl2.celery import udl2_conf
from edudl2.database.udl2_connector import UDL2DBConnection


def get_source_column_values_from_ref_column_mapping(source_table, load_type):
    """
    return all data for source_column from ref_column_mapping based on source_table value passed
    :param: source_table: source_table values to query for
    :return: A set containing all the columns expected in a source csv file
    """
    with UDL2DBConnection() as conn:
        table_meta = conn.get_table(udl2_conf['udl2_db']['ref_tables'][load_type])
        select_object = select([table_meta]).where(table_meta.c.source_table == source_table)
        return [row['source_column'] for row in conn.execute(select_object)]
