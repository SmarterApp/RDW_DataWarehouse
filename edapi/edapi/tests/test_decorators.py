'''
Created on Mar 14, 2013

@author: dip
'''
import unittest
from pyramid import testing
from pyramid.testing import DummyRequest
from edapi.decorators import user_info
from edapi.tests.dummy import DummyUser


@user_info
def some_func():
    return {}


@user_info
def some_func_with_some_results():
    return {'some': 'thing'}


class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_user_info(self):
        dummy_user = DummyUser()
        self.__config.testing_securitypolicy(dummy_user, ['TEACHER'])
        results = some_func()
        self.assertDictEqual(results, {'user_info': dummy_user.__dict__})

    def test_user_info_with_no_user(self):
        self.__config.testing_securitypolicy(None, ['TEACHER'])
        results = some_func()
        self.assertEqual(results, {})

    def test_user_with_some_results(self):
        dummy_user = DummyUser()
        self.__config.testing_securitypolicy(dummy_user, ['TEACHER'])
        results = some_func_with_some_results()
        self.assertEquals(len(results), 2)
        self.assertDictContainsSubset(some_func_with_some_results(), results)
        self.assertDictContainsSubset({'user_info': dummy_user.__dict__}, results)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
