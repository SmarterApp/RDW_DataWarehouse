'''

This module contains commonly-used functionality applied via Python decorators.

Created on Mar 13, 2013

@author: tosako
'''
import venusian
import pyramid
import validictory
from functools import wraps
from pyramid.security import authenticated_userid
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from edapi.validation import Validator
import io
from lxml import etree


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
            results['user_info'] = user
        return results
    return wrap


def validate_params(schema):
    '''
    :param schema: validictory style parameter schema
    '''
    def request_wrap(request_handler):
        '''
        :param request_handler: pyramid request handler
        '''
        @wraps(request_wrap)
        def validate_wrap(*args, **kwargs):
            '''
            :param args: function to accept an arbitrary number of arguments.
            :param kwargs: function to accept an arbitrary number of keyword arguments.
            '''
            params = {}
            request = None
            for arg in args:
                if type(arg) == pyramid.request.Request or type(arg) == pyramid.testing.DummyRequest:
                    try:
                        request = arg
                        params = Validator.fix_types_for_schema(schema.get('properties'), arg.GET, True)
                        if getattr(arg, 'method', 'GET') == 'POST' and len(arg.json_body) > 0:  # parse request params in POST
                            params.update(arg.json_body)
                    except ValueError:
                        raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')
                    except Exception as e:
                        raise EdApiHTTPPreconditionFailed('Payload cannot be parsed')
            # validate params against schema

            try:
                validictory.validate(params, schema)

                def validated(request):
                    '''
                    Return validated parameters for this request
                    '''
                    return params
                request.set_property(validated, 'validated_params', reify=True)
            except Exception as e:
                raise EdApiHTTPPreconditionFailed(e)
            return request_handler(*args, **kwargs)

        return validate_wrap

    return request_wrap


def validate_xml(xsd):
    '''
    validating xml against xsd
    '''
    xmlschema = None
    if xsd is not None:
        xsd_f = io.BytesIO(bytes(xsd, 'UTF-8'))
        xsd_doc = etree.parse(xsd_f)
        xmlschema = etree.XMLSchema(xsd_doc)

    def request_wrap(request_handler):
        '''
        :param request_handler: pyramid request handler
        '''
        @wraps(request_wrap)
        def validate_wrap(*args, **kwargs):
            for arg in args:
                if type(arg) == pyramid.request.Request or type(arg) == pyramid.testing.DummyRequest:
                    valid = False
                    try:
                        xml_body = arg.body
                        #for UT, if xmlschema is None, we do not validate
                        if xmlschema is None:
                            valid = True
                        else:
                            if type(arg) == pyramid.testing.DummyRequest:
                                xml_f = io.BytesIO(bytes(xml_body, 'utf-8'))
                            else:
                                xml_f = arg.body_file
                            xml_doc = etree.parse(xml_f)
                            if xmlschema.validate(xml_doc):
                                valid = True
                    except:
                        raise EdApiHTTPPreconditionFailed('Invalid XML by xsd')
                    if not valid:
                        raise EdApiHTTPPreconditionFailed('Invalid XML by xsd')
            return request_handler(xml_body)
        return validate_wrap
    return request_wrap
