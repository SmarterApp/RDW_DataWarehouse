'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.security.roles.default import DefaultRole
from smarter.security.context_role_map import ContextRoleMap
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing


class TestContextRoleMap(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        reg.settings = {}
        reg.settings['disable.context.security'] = 'False'
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        testing.tearDown()

    def test_get_context_with_no_role(self):
        context = ContextRoleMap.get_context("invalid")
        self.assertEqual(context, DefaultRole)

    def test_get_context_with_context_security_disabled(self):
        self.__config.registry.settings['disable.context.security'] = 'True'
        context = ContextRoleMap.get_context('TEACHER')
        self.assertEqual(context, DefaultRole)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
