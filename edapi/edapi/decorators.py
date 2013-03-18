'''
Created on Mar 13, 2013

@author: tosako
'''
import venusian
import pyramid
from functools import wraps
from pyramid.security import authenticated_userid


class report_config(object):
    '''
    used for processing decorator '@report_config' in pyramid scans
    '''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, original_func):
        settings = self.__dict__.copy()

        def callback(scanner, name, obj):
            def wrapper(*args, **kwargs):
                return original_func(self, *args, **kwargs)
            scanner.config.add_report_config((obj, original_func), **settings)
        venusian.attach(original_func, callback, category='edapi')
        return original_func


def user_info(orig_func):
    '''
    Append user_info to the returning result
    This returns User name and roles
    '''
    @wraps(orig_func)
    def wrap(*args, **kwds):
        results = orig_func(*args, **kwds)
        user = authenticated_userid(pyramid.threadlocal.get_current_request())
        # Only append user info if we get an User object returned
        if user:
            results['user_info'] = user.__dict__
        return results
    return wrap
