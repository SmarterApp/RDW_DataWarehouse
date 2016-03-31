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

'''
Created on Dec 5, 2013

@author: dip
'''
from collections import OrderedDict


def format_json(mapping):
    '''
    Given a python OrderedDictthat has keys with dot notation, expand it to return JSON that is ordered
    ex. {"one.two.three": "3"} produces {"one": {"two": {"three": "3"} } }

    :params OrderedDict mapping
    '''
    formatted = OrderedDict()
    for key, value in mapping.items():
        splitted_keys = key.split('.')
        set_value(formatted, splitted_keys, value)
    return formatted


def set_value(mapping, keys, value):
    '''
    Helper function that recursively sets the value of a python dictionary given a list of keys
    ex. keys = ["one", "two", "three"]
    returns {"one": {"two": {"three": 3 } } }
    '''
    current = keys[0]
    if len(keys) > 1:
        if mapping.get(current) is None:
            mapping[current] = OrderedDict()
        keys.remove(current)
        set_value(mapping[current], keys, value)
    else:
        if value is None:
            value = ''
        # We convert everything to a string
        mapping[current] = str(value)
