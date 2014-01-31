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


def delete_multiple_entries_from_dictionary_by_list_of_keys(dictionary, list_of_key_names):
    '''
    remove list of fields from any dictionary object
    also suppress delete not existing exceptions to make code easier to run
    :param dictionary: a dict object
    :param list_of_key_name: an array of dictionary keys that we try to delete
    '''
    for key_name in list_of_key_names:
        try:
            del dictionary[key_name]
        except Exception as e:
            pass
    return dictionary


def reverse_map(map_object):
    '''
    reverse map for a dict object
    '''
    _map = deepcopy(map_object)
    return {v: k for k, v in _map.items()}
