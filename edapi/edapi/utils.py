'''
Created on Jan 16, 2013

@author: aoren
'''
import logging


logger = logging.getLogger(__name__)


class ContentTypePredicate(object):
    '''
    Custom predicate for routing by content-type
    '''
    def __init__(self, content_type, config):
        self.content_type = content_type.lower()

    @staticmethod
    def default_content_type():
        return 'text/html'

    def text(self):
        return 'content_type = %s' % (self.content_type,)

    phash = text

    def __call__(self, context, request):
        content_type = getattr(request, 'content_type', None)
        # content-type in query param of a GET request trumps content-type found in request header
        params = request.GET
        if params and params.get('content-type') is not None:
            content_type = params.get('content-type')
        if not content_type or len(content_type) == 0:
            content_type = ContentTypePredicate.default_content_type()
        return content_type.lower() == self.content_type


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


def get_dict_value(dictionary, key, exception_to_raise=Exception):
    '''
    Dict lookup and raises an exception if key doesn't exist

    :param dictionary: the dictionary object
    :type dictionary: dict
    :param key: the key
    :type key: string
    :param exception_to_raise: the exception we throw if the key is not found
    :type exception_to_raise: exception
    '''
    value = dictionary.get(key)
    if (value is None):
        raise exception_to_raise(key)
    return value


def add_configuration_header(params_config):
    '''
    Turns the schema into an well-formatted JSON schema by adding a header.

    :param params_config: the original config json
    :return: a well formatted json
    '''
    result = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "schema-title",  # TODO: move to configuration
        "description": "schema-description",  # TODO: move to configuration
        "type": "object",
        "properties": params_config}

    return result


from functools import update_wrapper, wraps


class decorator_adapter(object):
    '''
    Adapter for decorator used for instance methods and functions
    '''
    def __init__(self, decorator, func):
        update_wrapper(self, func)
        self.decorator = decorator
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)

    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))


def adopt_to_method_and_func(decorator):
    @wraps(decorator)
    def adapter(func):
        return decorator_adapter(decorator, func)
    return adapter


def convert_query_string_to_dict_arrays(request_query_string):
    '''
    Becuase pyramid.GET.mixed() doesn't put param1=value1 as params1:[values1],
    so we need this to convert query string parameters into what we want.
    :param request_query_string: pyramid.request's query string dictionary object
    '''
    params = {}
    for k, v in request_query_string.items():
        if type(v) is not list:
            if params.get(k) is not None:
                params[k].append(v)
            else:
                params[k] = [v]
        else:
            params[k] = v
    return params
