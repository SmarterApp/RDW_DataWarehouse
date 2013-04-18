'''
Created on Apr 18, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite_no_data_load
from smarter import heartbeat
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPOk


class TestHeartbeat(Unittest_with_smarter_sqlite_no_data_load):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testValidHeartbeat(self):
        results = heartbeat.heartbeat(DummyRequest())
        self.assertIsInstance(results, HTTPOk)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
