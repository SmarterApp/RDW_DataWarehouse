# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

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
