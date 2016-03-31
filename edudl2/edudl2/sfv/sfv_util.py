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
