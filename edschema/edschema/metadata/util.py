'''
Created on Mar 21, 2014

@author: agrebneva
'''

#TODO: good place for it
NATURAL_KEY_ATTR = 'natural_key'
META_COLUMN = 'MetaColumn'


def get_natural_key(table):
    '''
    Find the natural keys for the table by looking at all columns in the table with info attribute 'natural_key'

    :param table: SQLAlchemy table object
    '''
    natural_key = [column for column in table.columns if NATURAL_KEY_ATTR in column.info.keys()]
    return natural_key if len(natural_key) > 0 else None


def get_natural_key_columns(table):
    '''
    Find columns for the table marked with a info attribute 'natural_key'

    :param table: SQLAlchemy table object
    '''
    natural_key = get_natural_key(table)
    return None if natural_key is None else [c.name for c in natural_key]


def get_foreign_key_reference_columns(table):
    '''
    Find columns for the table that reference other tables

    :param table: SQLAlchemy table object
    '''
    columns = [column for column in table.columns if column.foreign_keys != set()]
    return columns if len(columns) > 0 else None


def get_meta_columns(table):
    '''
    Find columns for the table that are of type MetaColumn

    :param table: SQLAlchemy table object
    '''
    columns = [column for column in table.columns if column.__class__.__name__ == META_COLUMN]
    return columns if len(columns) > 0 else None


def get_primary_key_columns(table):
    '''
    Find primary key columns for the table

    :param table: SQLAlchemy table object
    '''
    columns = [column for column in table.primary_key]
    return columns if len(columns) > 0 else None


def get_matcher_key_columns(table):
    '''
    Find columns to match records in the table to detect duplicates

    return All_columns - (meta_columns + pk_columns)

    :param table: SQLAlchemy table object
    '''
    meta = get_meta_columns(table)
    meta = meta if meta is not None else []
    pk = get_primary_key_columns(table)
    pk = pk if pk is not None else []
    return list(set(table.columns) - set(meta + pk))


def get_matcher_key_column_names(table):
    '''
    Returns matcher key columns names as a list

    :param table: SQLAlchemy table object
    '''
    matcher_columns = get_matcher_key_columns(table)
    return None if matcher_columns is None else [c.name for c in matcher_columns]


def get_tables_starting_with(metadata, starts_with):
    '''
    Returns list of dim tables based on metadata

    :param metadata: SQLAlchemy metadata object
    :param starts_with: Table name starts with this prefix
    '''
    return [table.name for table in metadata.sorted_tables if table.name.startswith(starts_with)]
