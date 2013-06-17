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
    Decorator to register data endpoint under /data/{reportname}

    .. code-block:: python

        from decorators import report_config

        \'\'Expose /data/test_report endpoint with the specified params \'\'
        @report_config(name="test_report", params={"free_text_field": {"type": "string",
                                                                   "pattern": "^[a-z]$"
                                                                   },
                                               "numeric_field": {"type": "integer"},
                                               "optional_field": {"type": "integer",
                                                                  "required": False
                                                                  },
                                               "school_sizes": {"type": "integer", "name": "school_size_report"},
                                               "student_lists": {"name": "student_list_report"}
                                               }
                   )
        def generate(self, params):
    '''

    def __init__(self, **kwargs):
        '''
        :param kwargs: function to accept an arbitrary number of keyword arguments.
        '''
        self.__dict__.update(kwargs)

    def __call__(self, original_func):
        '''
        :param original_func: a reference to the wrapped function
        @type original_func: reference
        '''
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
        '''
        :param args: function to accept an arbitrary number of arguments.
        :param kwds: function to accept an arbitrary number of keyword arguments.
        '''
        results = orig_func(*args, **kwds)
        user = authenticated_userid(pyramid.threadlocal.get_current_request())
        # Only append user info if we get an User object returned
        if user:
            results['user_info'] = user.__dict__
        return results
    return wrap
