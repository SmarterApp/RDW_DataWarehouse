__author__ = 'sravi'

"""
Utility methods for CSV and JSON validators
"""

from sqlalchemy.sql import select
from edudl2.udl2.celery import udl2_conf
from edudl2.udl2_util.database_util import connect_db, get_sqlalch_table_object


def get_source_column_values_from_ref_column_mapping(source_table, load_type):
    """
    return all data for source_column from ref_column_mapping based on source_table value passed
    :param: source_table: source_table values to query for
    :return: A set containing all the columns expected in a source csv file
    """
    (conn, engine) = connect_db(udl2_conf['udl2_db']['db_driver'],
                                udl2_conf['udl2_db']['db_user'],
                                udl2_conf['udl2_db']['db_pass'],
                                udl2_conf['udl2_db']['db_host'],
                                udl2_conf['udl2_db']['db_port'],
                                udl2_conf['udl2_db']['db_database'])

    table_meta = get_sqlalch_table_object(engine, udl2_conf['udl2_db']['reference_schema'],
                                          udl2_conf['udl2_db']['ref_tables'][load_type])

    select_object = select([table_meta]).where(table_meta.c.source_table == source_table)
    return [row['source_column'] for row in conn.execute(select_object)]
