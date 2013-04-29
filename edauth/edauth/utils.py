'''
Created on Feb 25, 2013

@author: dip
'''


def convert_to_int(value):
    '''
    converts a string value to int, returns None if value is None
    @param value: the converted value
    '''
    converted_value = None
    if value is not None:
        try:
            converted_value = int(value)
        except ValueError:
            return None
    return converted_value


def to_bool(val):
    '''
    boolean True/False converter
    @param val: the converted value
    '''
    return val and val.lower() in ('true', 'True')


def enum(*sequential, **named):
    '''
    enum
    '''
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)
