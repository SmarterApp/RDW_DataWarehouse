'''
Created on Jun 20, 2013

@author: dip
'''
from smarter.reports.compare_pop_report import get_state_view_report,\
    get_district_view_report


def get_state_view_namespace():
    '''
    Returns the namespace used to cache state view report
    '''
    return __get_namespace_name(get_state_view_report)


def get_district_view_namespace():
    '''
    Returns the namespace used to cache district view report
    '''
    return __get_namespace_name(get_district_view_report)


def __get_namespace_name(func):
    '''
    Returns the namespace of a function that was cached by Beaker by cache_region decorator
    
    :param func:  reference to the function that was decorated using cache_region decorator
    '''
    return func._arg_namespace
