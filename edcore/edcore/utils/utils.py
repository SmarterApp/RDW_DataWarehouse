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


def multi_delete(dictionary, list_of_key_names):
    '''
    remove list of fields from any dictionary object
    :param dictionary: a dict object
    :param list_of_key_name: an array of dictionary key
    '''
    for key_name in list_of_key_names:
        try:
            del dictionary[key_name]
        except Exception as e:
            pass
    return dictionary
