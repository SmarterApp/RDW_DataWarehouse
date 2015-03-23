'''
Created on Mar 23, 2015

'''
import unittest
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite
from smarter_score_batcher.services.heartbeat import heartbeat, check_datasource, check_celery
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPServerError


class TestHeartbeat(Unittest_with_tsb_sqlite):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testValidCelery(self):
        '''
        During unit test, the celery doesn't run. So it should fail
        '''
        results = check_celery(DummyRequest())
        self.assertIsInstance(results, HTTPServerError)

    def testValidDataSource(self):
        ok = check_datasource()
        self.assertTrue(ok)

    def testValidHeartbeat(self):
        '''
        During unit test, the celery doesn't run. So it should fail
        '''
        results = heartbeat(DummyRequest())
        self.assertIsInstance(results, HTTPServerError)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
