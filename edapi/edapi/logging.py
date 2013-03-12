'''
Created on Mar 5, 2013

@author: aoren, agrebneva
'''

import json
import re
from collections import OrderedDict
import logging
import pyramid
from edapi.utils import adopt_to_method_and_func
from functools import wraps


def audit_event(logger_name="audit"):
    log = logging.getLogger(logger_name)
    '''
    the function to be decorated is not passed to the constructor!.
    '''
    @adopt_to_method_and_func
    def wrapper(original_func):
        pos_arg_names = original_func.__code__.co_varnames[:original_func.__code__.co_argcount]
        func_name = original_func.__name__

        @wraps
        def __wrapper(*args, **kwds):
            # Log the entry into the function
            allargs = dict({'callable': func_name})
            for i in range(len(args)):
                allargs[pos_arg_names[i]] = args[i]
            allargs.update(kwds)
            if not 'user' in allargs.keys():
                allargs["user"] = pyramid.security.effective_principals(pyramid.threadlocal.get_current_request())
            log.info(allargs)
            return original_func(*args, **kwds)
        return __wrapper

    return wrapper


class JsonDictLoggingFormatter(logging.Formatter):
    '''Json logging formatter'''
    def __init__(self, fmt=None):
        logging.Formatter.__init__(self, fmt)
        self.fmt_tkn = re.compile(r'\((.*?)\)', re.IGNORECASE).findall(self._fmt)

    def format(self, record):
        """Formats a log record and serializes to json"""
        loggable = OrderedDict()
        if self.usesTime():
            loggable["asctime"] = self.formatTime(record, self.datefmt)

        for key, value in record.__dict__:
            if isinstance(value, dict):
                loggable.update(value)
            else:
                loggable[key] = value

        return json.dumps(loggable)
