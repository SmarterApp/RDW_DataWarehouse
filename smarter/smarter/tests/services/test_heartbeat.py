'''
Created on Apr 18, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite_no_data_load,\
    get_test_tenant_name
from smarter.services import heartbeat
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPOk
import smarter


class TestHeartbeat(Unittest_with_smarter_sqlite_no_data_load):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testValidHeartbeat(self):
        global TENANTS
        smarter.TENANTS = [get_test_tenant_name()]
        results = heartbeat.heartbeat(DummyRequest())
        self.assertIsInstance(results, HTTPOk)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
