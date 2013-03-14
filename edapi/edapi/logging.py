'''
Created on Mar 5, 2013

@author: aoren, agrebneva
'''

import simplejson as json
import re
from collections import OrderedDict
import logging
import pyramid
from edapi.utils import adopt_to_method_and_func


def audit_event(logger_name="audit"):
    log = logging.getLogger(logger_name)
    '''
    the function to be decorated is not passed to the constructor!.
    '''
    @adopt_to_method_and_func
    def audit_event_wrapper(original_func):
        func_name = original_func.__name__
        class_name = None
        if hasattr(original_func, '__self__'):
            class_name = original_func.__self__.__class__.__name__

        def __wrapped(*args, **kwds):
            allargs = {'callable': func_name}
            # Log the entry into the function
            if not class_name is None:
                allargs['class'] = class_name
            params = {}
            params['args'] = args
            params.update(kwds)
            allargs['params'] = params
            if not 'user' in allargs.keys():
                allargs['user'] = pyramid.security.effective_principals(pyramid.threadlocal.get_current_request())
            log.info(allargs)
            return original_func(*args, **kwds)
        return __wrapped

    return audit_event_wrapper


class JsonDictLoggingFormatter(logging.Formatter):
    '''Json logging formatter'''

    def __init__(self, fmt=None, datefmt='%yyyymmdd %H:%M:%S'):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.fmt_tkn = re.compile(r'\((.*?)\)', re.IGNORECASE).findall(self._fmt)

    def format(self, record):
        '''Formats a log record and serializes to json'''
        loggable = OrderedDict()
        keys = record.__dict__
        for formatter in self.fmt_tkn:
            if formatter in keys:
                loggable[formatter] = record.__dict__[formatter]
        if self.usesTime():
            loggable['asctime'] = self.formatTime(record, self.datefmt)
        if isinstance(record.msg, dict):
            loggable['msg'] = record.msg
        else:
            loggable['msg'] = record.getMessage()
        return json.dumps(loggable)
