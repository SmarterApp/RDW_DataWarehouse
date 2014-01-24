'''
Created on Jun 27, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from edauth.security.session import Session
from smarter.services.trigger import trigger
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite_no_data_load
from edapi.httpexceptions import EdApiHTTPNotFound


class TestTrigger(Unittest_with_stats_sqlite_no_data_load):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        dummy_session = Session()
        dummy_session.set_roles(['SUPER_USER'])
        dummy_session.set_uid('272')
        dummy_session.set_tenants(['cat'])
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        testing.tearDown()

    def test_invalid_key(self):
        self.__request.matchdict['trigger_type'] = 'invalid'
        rtn = trigger(self.__request)
        self.assertIsInstance(rtn, EdApiHTTPNotFound)

    def test_cache_trigger(self):
        self.__request.matchdict['trigger_type'] = 'cache'
        rtn = trigger(self.__request)
        self.assertTrue(rtn['result'], 'OK')

    def test_pdf_trigger(self):
        self.__request.matchdict['trigger_type'] = 'pdf'
        rtn = trigger(self.__request)
        self.assertTrue(rtn['result'], 'OK')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
