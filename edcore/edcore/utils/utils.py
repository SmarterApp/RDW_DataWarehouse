'''
Created on Sep 1, 2013

@author: dip
'''
from copy import deepcopy


def merge_dict(d1, d2):
    '''
    merges two dictionary
    d1 overwrites d2
    '''
    combined = deepcopy(d2)
    combined.update(d1)
    return combined


def multi_delete(dictionary, list_of_field_names):
    '''
    remove list of fields from any dictionary object
    '''
    for field_name in list_of_field_names:
        try:
            del dictionary[field_name]
        except Exception as e:
            pass
    return dictionary
