from edmigrate.exceptions import EdMigrateRecordAlreadyDeletedException, EdMigrateRecordInsertionException
from edmigrate.utils.constants import Constants
from edmigrate.migrate.migrate_helper import yield_rows
from sqlalchemy.sql.expression import select, and_, tuple_
from edschema.metadata.util import get_natural_key_columns

import time

__author__ = 'sravi'


def migrate_by_row(batch_guid, batch_size, deactivate, dest_connector, source_connector, table_name):
    delete_count, insert_count = 0, 0
    source_table = source_connector.get_table(table_name)
    primary_key = source_table.primary_key.columns.keys()[0]
    # if there is a status column, it's a candidate for deletes
    has_status = Constants.STATUS in source_table.columns
    if has_status:
        delete_query = select([primary_key]).where(
            and_(source_table.c.batch_guid == batch_guid, source_table.c.rec_status == Constants.STATUS_DELETED))
        delete_count = _process_batch(source_connector, dest_connector, preprod_to_prod_delete_records, delete_query,
                                      table_name,
                                      primary_key, deactivate, batch_size)

    # for Insert
    insert_query = select([source_table]).where(source_table.c.batch_guid == batch_guid)
    if has_status:
        insert_query = insert_query.where(and_(source_table.c.rec_status == Constants.STATUS_CURRENT))
    insert_count = _process_batch(source_connector, dest_connector, preprod_to_prod_insert_records, insert_query,
                                  table_name,
                                  primary_key, deactivate, batch_size)
    return delete_count, insert_count


def _process_batch(source_connector, dest_connector, handler, query, table_name,
                   primary_key_field_name, deactivate, batch_size=100):
    '''Process each batch for the given handler and query
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param handler: function that handles the batch for the type (insert/delete)
    :param query: query for the source to select batch
    :param table_name: name of the table to be migrated
    :param primary_key_field_name: primary key for the table_name
    :batch batch of records to be deleted

    :returns number of record updated
    '''
    proxy_rows = yield_rows(source_connector, query, batch_size)
    total_count = 0
    # for rows in a scrollable cursor, preserve primary key
    for rows in proxy_rows:
        total_count += handler(source_connector, dest_connector,
                               table_name, primary_key_field_name, rows, deactivate)
    return total_count


def preprod_to_prod_delete_records(source_connector, dest_connector,
                                   table_name, primary_key_field_name, batch, deactivate):
    '''Process deletes for the batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param primary_key_field_name: primary key for the table_name
    :batch batch of records to be deleted

    :returns number of record updated
    '''
    # select primary keys to be deleted in destination
    primary_keys = [row[primary_key_field_name] for row in batch]
    batch_size = len(primary_keys)
    dest_table = dest_connector.get_table(table_name)
    dest_primary_key_field = dest_table.columns[primary_key_field_name]
    # set status to D if the status is C for all records in the batch
    update_query = dest_table.update(and_(dest_primary_key_field.in_(primary_keys), dest_table.c.rec_status == Constants.STATUS_CURRENT)).values(rec_status=Constants.STATUS_DELETED)
    # if number of updated records doesn't match, that means one of the records was changed from C to D by another batch
    if dest_connector.execute(update_query).rowcount != batch_size:
        raise EdMigrateRecordAlreadyDeletedException
    return batch_size


def deactivate_old_records(dest_connector, dest_table, natural_keys, batch):
    '''deactivates old records in the destination table based on matching records from batch using natural key combination
    :param dest_connector: Destination connection
    :param dest_table: name of the table to be migrated
    :param natural_keys: natural key combination for the dest_table
    :batch batch of records to be verified
    '''
    key_columns = [dest_table.columns[key] for key in natural_keys]
    key_values = [[row[key] for key in natural_keys] for row in batch]

    # update prod rec_status to inactive for records matching with the natural keys of the records in the current batch
    update_query = dest_table.update(and_(dest_table.c.rec_status == 'C',
                                          tuple_(*key_columns).in_(key_values))).values(rec_status='I',
                                                                                        to_date=time.strftime("%Y%m%d"))
    dest_connector.execute(update_query)


def preprod_to_prod_insert_records(source_connector, dest_connector, table_name,
                                   primary_key_field_name, batch, deactivate):
    '''Process inserts for the batch
    :param source_connector: Source connection
    :param dest_connector: Destination connection
    :param table_name: name of the table to be migrated
    :param primary_key_field_name: primary key for the table_name
    :batch batch of records to be inserted

    :returns number of record updated
    '''
    dest_table = dest_connector.get_table(table_name)
    natural_keys = get_natural_key_columns(dest_table)
    # the deactivate flag is needed to avoid the record deactivation query path in unit tests
    # this part is tested as part of function tests
    if deactivate and natural_keys is not None:
        deactivate_old_records(dest_connector, dest_table, natural_keys, batch)
    # insert the new records to prod with rec_status as current
    insert_query = dest_table.insert()
    records_inserted = dest_connector.execute(insert_query, batch).rowcount
    batch_size = len(batch)
    if records_inserted != batch_size:
        raise EdMigrateRecordInsertionException
    return batch_size
