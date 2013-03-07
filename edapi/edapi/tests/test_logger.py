'''
Created on Mar 6, 2013

@author: aoren
'''
from edapi.autolog import log_instance_method, log_function
from logging import INFO, DEBUG


@log_function(DEBUG, None, "test2")
def test_function(param1, param2):
    pass


@log_function(DEBUG, "test_display", "test3")
def test_display_name():
    pass


class TestLogger(object):

    @log_instance_method(INFO, None, "test")
    def test_method(self, param1, param2):
        pass
