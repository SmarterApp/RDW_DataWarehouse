'''
Helper functions to format names for display on reports

Created on Mar 4, 2013

@author: dwu
'''


def format_full_name(first_name, middle_name, last_name):
    '''
    Format a name to "<first> <middle init> <last>"
    '''
    if (middle_name is not None) and (len(middle_name) > 0):
        middle_init = middle_name[0] + '.'
    else:
        middle_init = ''
    return "{0} {1} {2}".format(first_name, middle_init, last_name).replace('  ', ' ')


def format_full_name_rev(first_name, middle_name, last_name):
    '''
    Format a name to "<last>, <first> <middle init>"
    '''
    if (middle_name is not None) and (len(middle_name) > 0):
        middle_init = middle_name[0] + '.'
    else:
        middle_init = ''
    return "{0}, {1} {2}".format(last_name, first_name, middle_init).replace('  ', ' ')
