'''
Created on Jul 13, 2013

@author: dip
'''
from beaker import util
from beaker.cache import cache_regions, Cache
import hashlib
from functools import wraps
import collections


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
    :param decor_args:  additional arguments used as cache key
    '''
    cache = {}

    def decorate(func):
        skip_self = util.has_self_arg(func)
        func_name = util.func_namespace(func)

        @wraps(func)
        def cached(*args):
            if type(region) is list:
                region_name = region[0]
            else:
                region_name = region

            if router is not None:
                region_name = router(*args)

            if cache.get(region_name) is None:
                reg = cache_regions.get(region_name)
                cache[region_name] = Cache._get_cache(namespace, reg)

            if key_generator is not None:
                combined_args = decor_args + key_generator(*args)
            else:
                if skip_self:
                    combined_args = decor_args + args[1:]
                else:
                    combined_args = decor_args + args

            cache_key = get_cache_key(combined_args, func_name)

            def go():
                return func(*args)

            return cache[region_name].get_value(cache_key, createfunc=go)
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
