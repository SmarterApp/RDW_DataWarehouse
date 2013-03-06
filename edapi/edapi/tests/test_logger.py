'''
Created on Mar 6, 2013

@author: aoren
'''
from edapi.autolog import log_instance_method, log_function
from logging import INFO


@log_function(INFO, None, "test2")
def test_function(param1, param2):
    pass


class TestLogger(object):

    @log_instance_method(INFO, None, "test")
    def test_method(self, param1, param2):
        pass
