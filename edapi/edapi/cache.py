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
Created on Jul 13, 2013

@author: dip
'''
from beaker import util
from beaker.cache import cache_regions, Cache
import hashlib
from functools import wraps
import collections
import json


def get_cache_key(args, func_name):
    '''
    Returns the cache key based on the function name and arguments

    :param args:  list of arguments
    :param func_name:  name of function obtained by util.func_namespace
    '''
    cache_key = " ".join(map(str, args))
    cache_key = (func_name + cache_key).encode()
    cache_key = hashlib.sha1(cache_key).hexdigest()
    return cache_key


def cache_region(region, namespace='smarter', router=None, key_generator=None, *decor_args):
    '''
    Custom cache region decorator for smarter

    :param region:  a list of region or a string representing a region
    :param namespace:  namespace name
    :param router:  a reference to a function that returns a region name for region routing needs
    :param key_generator:  a reference to a function that returns a tuple representing the cache key
    :param decor_args:  additional arguments used as cache key

    Example::

        @cache_region('region1')
        def read_from_db(id, field, value)
            return database.query(id, field, value)

    This will cache results to region1 and the cache key will be on paramter values

    Example::

        @cache_region(['region1' 'region2'], router=get_region, key_generator=get_key_generator)
        def read_from_db(id, field, value)
            return database.query(id, field, value)

    This will setup two cache regions, and will call get_region function that will return the region name for route cache results to
    It will generate the cache key get_key_generator()
    '''
    cache = {}

    def decorate(func):
        skip_self = util.has_self_arg(func)
        func_name = util.func_namespace(func)

        @wraps(func)
        def cached(*args):
            region_name = region[0] if type(region) is list else region
            # If router exist, use it to determine the cache region
            if router is not None:
                region_name = router(*args)
            if region_name is None:
                return func(*args)

            if cache.get(region_name) is None:
                reg = cache_regions.get(region_name)
                cache[region_name] = Cache._get_cache(namespace, reg)
            # If key generator exists, use it to generate a key
            if key_generator is not None:
                combined_args = decor_args + key_generator(*args)
            else:
                combined_args = decor_args + args[1:] if skip_self else args

            cache_key = get_cache_key(combined_args, func_name)

            def go():
                value = func(*args)
                # jsonify object to avoid pickle to get better performance
                return json.dumps(value)

            value = cache[region_name].get_value(cache_key, createfunc=go)
            return json.loads(value)
        cached._func_name = func_name
        return cached
    return decorate


def region_invalidate(func, region, *args, namespace='smarter'):
    '''
    Invalidates a cache region

    :param func:  reference to a func
    :param region:  name of the region
    :param arg:  list of positional arguments
    :param namespace:  the namespace that is prepended in cache key
    '''
    reg = cache_regions.get(region)
    if reg is None:
        raise KeyError
    try:
        if isinstance(func, collections.Callable):
            func_name = func._func_name
    except:
        raise KeyError
    cache = Cache._get_cache(namespace, reg)
    cache_key = get_cache_key(args, func_name)
    cache.remove_value(cache_key)
