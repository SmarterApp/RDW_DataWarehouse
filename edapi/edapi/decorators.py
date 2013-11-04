'''

This module contains commonly-used functionality applied via Python decorators.

Created on Mar 13, 2013

@author: tosako
'''
import venusian
import pyramid
import types
import validictory
import json
from functools import wraps
from pyramid.security import authenticated_userid
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from edapi.validation import Validator


class report_config(object):
    '''
    Decorator to configure and register a data endpoint under /data/{reportname}.

    :param kwargs: "name" specifies the name of the report.
                   "params" specifies report input parameters, and must follow the
                   JSON Schema conventions used by the Python Validictory library.
    :type kwargs: key-value pairs

    Example:

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
    Decorator to append user name and roles to returned data.
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


def validate_params(method, schema):
    '''
    :param schema: validictory style parameter schema
    '''
    def request_wrap(request_handler):
        '''
        :param request_handler: pyramid request handler
        '''
        def validate_wrap(*args, **kwargs):
            '''
            :param args: function to accept an arbitrary number of arguments.
            :param kwargs: function to accept an arbitrary number of keyword arguments.
            '''
            params = {}
            for arg in args:
                if type(arg) == pyramid.request.Request:
                    if method == 'GET':
                        query_string = arg.GET
                        # flat construsct json
                        for k, v in query_string.items():
                            if params.get(k) is not None:
                                params[k].append(v)
                            else:
                                params[k] = [v]

                    # jsonify request params in GET
                    elif method == 'POST':
                        try:
                            params = json.loads(arg.json_body)
                        except ValueError:
                            raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')
            # validate params against schema

            try:
                validictory.validate(params, schema)
            except Exception as e:
                raise EdApiHTTPPreconditionFailed("Parameters validation failed")

            return request_handler(*args, **kwargs)

        return validate_wrap

    return request_wrap
