'''
Created on Apr 18, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite_no_data_load
from smarter.services import heartbeat
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPOk, HTTPServerError


class TestHeartbeat(Unittest_with_edcore_sqlite_no_data_load):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testValidDataSource(self):
        results = heartbeat.check_datasource(DummyRequest())
        self.assertIsInstance(results, HTTPOk)

    def testValidCelery(self):
        '''
        During unit test, the celery doesn't run. So it should fail
        '''
        results = heartbeat.check_celery(DummyRequest())
        self.assertIsInstance(results, HTTPServerError)

    def testValidHeartbeat(self):
        '''
        During unit test, the celery doesn't run. So it should fail
        '''
        results = heartbeat.heartbeat(DummyRequest())
        self.assertIsInstance(results, HTTPServerError)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
