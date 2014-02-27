'''
Created on Aug 29, 2013

@author: dawu
'''
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite_no_data_load
from edapi.tests.dummy import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from smarter.services.userinfo import user_info_service
import unittest
from edauth.tests.test_helper.create_session import create_test_session


class TestUserInfo(Unittest_with_stats_sqlite_no_data_load):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        self.__request.registry = reg
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        dummy_session = create_test_session(['SUPER_USER'], uid='272', tenant='cat')
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        testing.tearDown()

    def test_get_user_info(self):
        data = user_info_service(self.__request)
        user = data.get('user_info')
        self.assertIsNotNone(user, "User info should not be empty")
        self.assertEqual('272', user.get('_Session__user').get_uid(), "User guid doesn't match")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
