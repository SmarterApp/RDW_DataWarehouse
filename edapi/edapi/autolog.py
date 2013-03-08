'''
Created on Mar 5, 2013

@author: aoren
'''

#from edapi import utils
from logging import INFO
import logging


def shorten_string(obj):
    '''
    Where to put gritty heuristics to make an object appear in most useful
    form. defaults to __str__.
    '''
    if "wx." in str(obj.__class__) or obj.__class__.__name__.startswith("wx"):
        shortclassname = obj.__class__.__name__
        if hasattr(obj, "blockItem") and hasattr(obj.blockItem, "blockName"):
            moreInfo = "block:'{0}'".format(obj.blockItem.blockName)
        else:
            moreInfo = "at {0}".format(id(obj))
        return "<{0} {1}>".format(shortclassname, moreInfo)
    else:
        return str(obj)


def format_all_args(args, kwds):
    '''
    makes a nice string representation of all the arguments
    '''
    allargs = []
    for item in args:
        allargs.append('{0}'.format(shorten_string(item)))
    for key, item in kwds.items():
        allargs.append('{0}={1}'.format(key, shorten_string(item)))
    formattedArgs = ', '.join(allargs)
    return formattedArgs


class log_function(object):
    '''
    Logs a function name and the arguments it was called with
    '''
    def __init__(self, level=INFO, display_name=None, logger_name=None, report_name=""):
        """
        the function to be decorated is not passed to the constructor!.
        """
        self.level = level
        self.display_name = display_name
        self.logger_name = logger_name
        self.report_name = report_name

    def __call__(self, original_func):
        """
        __call__() is only called once, as part of the decoration process! It hasa single argument,
        which is the function object.
        """
        if not self.display_name:
            self.display_name = original_func.__name__

        def __wrapper(*args, **kwds):
            argstr = format_all_args(args, kwds)

            log = get_logger(self.logger_name)
            # Log the entry into the function
            log.log(self.level, "{2}: {0} ({1}) ".format(self.display_name, argstr, self.report_name))

            return original_func(*args, **kwds)
        return __wrapper


class log_instance_method(object):
    '''
    Logs an instance method name, its class name and the arguments it was called with
    '''
    def __init__(self, level=INFO, display_name=None, logger_name=None):
        """
        the function to be decorated is not passed to the constructor!.
        """
        self.level = level
        self.display_name = display_name
        self.logger_name = logger_name

    def __call__(self, original_func):
        """
        __call__() is only called once, as part of the decoration process! It hasa single argument,
        which is the function object.
        """
        if not self.display_name:
            self.display_name = original_func.__name__

        def __wrapper(*args, **kwds):
            argstr = format_all_args(args, kwds)
            self_str = shorten_string(self)

            log = get_logger(self.logger_name)
            # Log the entry into the method
            log.log(self.level, "{0}{1} ({2}) ".format(self_str, self.display_name, argstr))

            return original_func(*args, **kwds)
        return __wrapper


def get_logger(name=None, add_file_handler=True):
    '''
    Gets a logger by name, and add a file handler, with the same name, to it
    '''
    # if no name is provided we use the module name
    if name is None:
        name = __name__

    logger = logging.getLogger(name)

    # if there are no handlers we add a file handler with the given name
    if add_file_handler and len(logger.handlers) == 0:
        # create file handler which logs even debug messages
        # TODO: add configurable folder
        fh = logging.FileHandler('{0}.log'.format(name))
        fh.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)

    return logger
