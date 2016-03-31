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
from smarter.security.roles.base import BaseRole
from pyramid.security import Allow
from smarter_common.security.constants import RolesConstants
import edauth
from edcore.tests.utils.unittest_with_edcore_sqlite import get_unittest_tenant_name,\
    UnittestEdcoreDBConnection, Unittest_with_edcore_sqlite
from edcore.security.tenant import set_tenant_map
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from pyramid.testing import DummyRequest
from pyramid import testing


class TestBase(Unittest_with_edcore_sqlite):

    def setUp(self):
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout')),
                         (Allow, RolesConstants.SAR_EXTRACTS, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        self.tenant = get_unittest_tenant_name()
        set_tenant_map({self.tenant: "NC"})
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), "NC", "228", "242"),
                                        RoleRelation(RolesConstants.SAR_EXTRACTS, get_unittest_tenant_name(), "NC", "228", "242")])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)

    def test_check_context(self):
        with UnittestEdcoreDBConnection() as connection:
            base = BaseRole(connection, 'base')
            context = base.check_context(self.tenant, self.user, ['nostudent'])
            self.assertFalse(context)

    def test_check_context_with_context(self):
        with UnittestEdcoreDBConnection() as connection:
            base = BaseRole(connection, RolesConstants.PII)
            student_ids = ['e2f3c6a5-e28b-43e8-817b-fc7afed02b9b']
            context = base.check_context(self.tenant, self.user, student_ids)
            self.assertTrue(context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
