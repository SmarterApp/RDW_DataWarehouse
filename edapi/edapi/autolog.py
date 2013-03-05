'''
Created on Mar 5, 2013

@author: aoren
'''

from edapi import utils
from logging import INFO


def shorten_string(obj):
    """
    Where to put gritty heuristics to make an object appear in most useful
    form. defaults to __str__.
    """
    if "wx." in str(obj.__class__)  or  obj.__class__.__name__.startswith("wx"):
        shortclassname = obj.__class__.__name__
        if hasattr(obj, "blockItem") and hasattr(obj.blockItem, "blockName"):
            moreInfo = "block:'{0}'".format(obj.blockItem.blockName)
        else:
            moreInfo = "at {0}".format(id(obj))
        return "<{0} {1}>".format(shortclassname, moreInfo)
    else:
        return str(obj)


def format_all_args(args, kwds):
    """
    makes a nice string representation of all the arguments
    """
    allargs = []
    for item in args:
        allargs.append('{0}'.format(shorten_string(item)))
    for key, item in kwds.items():
        allargs.append('{0}={1}'.format(key, shorten_string(item)))
    formattedArgs = ', '.join(allargs)
    return formattedArgs


class log_function(object):
    def __init__(self, level=INFO, display_name=None, logger_name=None):
        """a decorator."""
        self.level = level
        self.display_name = display_name
        self.logger_name = logger_name

    def __call__(self, original_func):
        """a decorator."""
        if not self.display_name:
            self.display_name = original_func.__name__

        def __wrapper(*args, **kwds):
            argstr = format_all_args(args, kwds)

            log = utils.get_logger(self.logger_name)
            # Log the entry into the function
            log.log(self.level, "{0} ({1}) ".format(self.display_name, argstr))

            return original_func(*args, **kwds)
        return __wrapper


class log_instance_method(object):
    def __init__(self, level=INFO, display_name=None, logger_name=None):
        """a decorator."""
        self.level = level
        self.display_name = display_name
        self.logger_name = logger_name

    def __call__(self, original_func):
        """a decorator."""
        if not self.display_name:
            self.display_name = original_func.__name__

        def __wrapper(*args, **kwds):
            argstr = format_all_args(args, kwds)
            self_str = shorten_string(self)

            log = utils.get_logger(self.logger_name)
            # Log the entry into the method
            log.log(self.level, "{0}{1} ({2}) ".format(self_str, self.display_name, argstr))

            return original_func(*args, **kwds)
        return __wrapper
