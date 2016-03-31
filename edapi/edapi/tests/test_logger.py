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
Created on Mar 6, 2013

@author: aoren
'''
from edapi.logging import audit_event, SkipUnsupportedEncoder
import unittest
import json


@audit_event(logger_name="test")
def test_function(param1, param2):
    pass


@audit_event(logger_name="test", blacklist_args=["param1"])
def test_blacklist_param(param1, param2):
    pass


@audit_event(logger_name="test", blacklist_args=["param3"])
def test_blacklist_non_existing_param(param1, param2):
    pass


@audit_event(logger_name="test")
def test_blacklist_global_param(first_name, last_name, param1, param2):
    pass


@audit_event(logger_name="test")
def test_display_name():
    pass


class TestLogger(object):

    @audit_event(logger_name="test")
    def test_method(self, param1, param2):
        pass


class TestAudit(unittest.TestCase):

    def test_not_exception_for_unserializable(self):
        test_blacklist_global_param("string", "string", SkipUnsupportedEncoder(), test_blacklist_non_existing_param)

    def test_encoder(self):
        loggable = {"string", "string", SkipUnsupportedEncoder(), test_blacklist_non_existing_param}
        self.assertRaises(TypeError, json.dumps, (loggable))
        json.dumps(loggable, cls=SkipUnsupportedEncoder)


if __name__ == "__main__":
    unittest.main()
