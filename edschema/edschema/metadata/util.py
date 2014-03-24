'''
Created on Mar 21, 2014

@author: agrebneva
'''


def get_natural_key(table):
    '''
    Find first index for the table marked with a custom attribute 'natural_key'
    '''
    natural_key = [index for index in table.indexes if 'natural_key' in index.kwargs.keys() and index.kwargs['natural_key']]
    return natural_key[0] if len(natural_key) > 0 else None


def get_natural_key_columns(table):
    '''
    Find columns for the first index for the table marked with a custom attribute 'natural_key'
    '''
    natural_key = get_natural_key(table)
    return None if natural_key is None else natural_key.columns
