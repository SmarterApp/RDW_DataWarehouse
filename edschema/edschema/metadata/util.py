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
    return [column for column in table.columns if NATURAL_KEY_ATTR in column.info.keys()]


def get_natural_key_columns(table):
    '''
    Find columns for the table marked with a info attribute 'natural_key'

    :param table: SQLAlchemy table object
    '''
    return [c.name for c in get_natural_key(table)]


def get_foreign_key_reference_columns(table):
    '''
    Find columns for the table that reference other tables

    :param table: SQLAlchemy table object
    '''
    return [column for column in table.columns if column.foreign_keys != set()]


def get_meta_columns(table):
    '''
    Find columns for the table that are of type MetaColumn

    :param table: SQLAlchemy table object
    '''
    return [column for column in table.columns if getattr(column, "col_type", "Column") == META_COLUMN]


def get_primary_key_columns(table):
    '''
    Find primary key columns for the table

    :param table: SQLAlchemy table object
    '''
    return [column for column in table.primary_key]


def get_matcher_key_columns(table):
    '''
    Find columns to match records in the table to detect duplicates

    returns [all_columns - (meta_columns + pk_columns + fk_columns)]

    :param table: SQLAlchemy table object
    '''
    return list(set(table.columns) - set(get_meta_columns(table) +
                                         get_primary_key_columns(table) +
                                         get_foreign_key_reference_columns(table)))


def get_matcher_key_column_names(table):
    '''
    Returns matcher key columns names as a list

    :param table: SQLAlchemy table object
    '''
    return [c.name for c in get_matcher_key_columns(table)]


def get_tables_starting_with(metadata, prefix):
    '''
    Returns list of tables starting with prefix based on metadata

    :param metadata: SQLAlchemy metadata object
    :param prefix: prefix string
    '''
    return [table.name for table in metadata.sorted_tables if table.name.startswith(prefix)]
