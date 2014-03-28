'''
Created on Mar 27, 2014

@author: tosako
'''
import logging


class MockLogger(logging.Logger):

    def __init__(self, *args, **kwargs):
        self.logged = []
        logging.Logger.__init__(self, *args, **kwargs)

    def _log(self, level, msg, args, **kwargs):
        self.logged.append((level, msg, args, kwargs))
