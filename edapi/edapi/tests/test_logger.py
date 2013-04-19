'''
Created on Mar 6, 2013

@author: aoren
'''
from edapi.logging import audit_event


@audit_event("test", logger_name="test")
def test_function(param1, param2):
    pass


@audit_event("test", logger_name="test")
def test_display_name():
    pass


class TestLogger(object):

    @audit_event("test", logger_name="test")
    def test_method(self, param1, param2):
        pass
