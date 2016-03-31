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

from edmigrate.migrate.migrate_helper import yield_rows
from sqlalchemy.sql.expression import select, and_
import json

__author__ = 'ablum'


def migrate_snapshot(dest_connector, source_connector, table_name, batch_criteria, batch_size):
    """
    Migrate a table snapshot as part of a migration by batch.

    @param dest_connector: Destination DB connector
    @param source_connector: Source DB connector
    @param table_name: Name of table to migrate
    @param batch_criteria: Deletion criteria for destination table.

    @return: Deletion and insertion row counts
    """

    # Delete old rows.
    dest_table = dest_connector.get_table(table_name)
    delete_query = _create_delete_query(batch_criteria, dest_table)
    delete_count = dest_connector.execute(delete_query).rowcount

    # Insert new rows.
    source_table = source_connector.get_table(table_name)
    batched_rows = yield_rows(source_connector, select([source_table]), batch_size)

    insert_count = 0
    for rows in batched_rows:
        insert_query = dest_table.insert()
        insert_count += dest_connector.execute(insert_query, rows).rowcount

    return delete_count, insert_count


def _create_delete_query(batch_criteria, dest_table):
    snapshot_criteria = json.loads(batch_criteria)

    delete_query = dest_table.delete()

    for k, v in snapshot_criteria.items():
        delete_query = delete_query.where(and_(dest_table.c[k] == v))

    return delete_query
