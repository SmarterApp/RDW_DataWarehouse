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
