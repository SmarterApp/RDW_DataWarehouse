'''
Created on Mar 21, 2014

@author: agrebneva
'''

#TODO: good place for it
NATURAL_KEY_ATTR = 'natural_key'


def get_natural_key(table):
    '''
    Find the natural keys for the table by looking at all columns in the table with info attribute 'natural_key'
    '''
    natural_key = [column for column in table.columns if 'natural_key' in column.info.keys()]
    return natural_key if len(natural_key) > 0 else None


def get_natural_key_columns(table):
    '''
    Find columns for the table marked with a info attribute 'natural_key'
    '''
    natural_key = get_natural_key(table)
    return None if natural_key is None else [c.name for c in natural_key]


def get_foreign_key_reference_columns(table):
    '''
    Find columns for the table that reference other tables
    '''
    columns = [column for column in table.columns if column.foreign_keys != set()]
    return columns if len(columns) > 0 else None
