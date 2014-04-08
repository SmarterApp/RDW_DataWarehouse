'''
Created on May 9, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from sqlalchemy.sql.expression import select
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.srs_extracts import SRSExtracts
from pyramid.security import Allow
from smarter.security.constants import RolesConstants
import edauth
from edcore.security.tenant import set_tenant_map
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from pyramid.testing import DummyRequest
from pyramid import testing


class TestSRSContextSecurity(Unittest_with_edcore_sqlite):

    def setUp(self):
        defined_roles = [(Allow, RolesConstants.SRS_EXTRACTS, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        self.tenant = get_unittest_tenant_name()
        set_tenant_map({self.tenant: 'ES'})
        dummy_session = create_test_session([RolesConstants.SRS_EXTRACTS])
        dummy_session.set_user_context([RoleRelation(RolesConstants.SRS_EXTRACTS, self.tenant, None, None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)

    def test_get_srs_context_tenant_level(self):
        with UnittestEdcoreDBConnection() as connection:
            srs = SRSExtracts(connection, RolesConstants.SRS_EXTRACTS)
            clause = srs.get_context(self.tenant, self.user)
            self.assertEqual(len(clause), 0)

    def test_get_srs_context_state_level(self):
        dummy_session = create_test_session([RolesConstants.SRS_EXTRACTS])
        dummy_session.set_user_context([RoleRelation(RolesConstants.SRS_EXTRACTS, self.tenant, 'ES', None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            student_reg = connection.get_table(Constants.STUDENT_REG)
            query = select([student_reg.c.school_guid],
                           from_obj=([student_reg]))
            srs = SRSExtracts(connection, RolesConstants.SRS_EXTRACTS)
            clause = srs.get_context(self.tenant, self.user)
            self.assertEqual(len(clause), 1)
            query = query.where(*clause)
            result = connection.get_result(query)
            self.assertEqual(len(result), 2581)

    def test_get_srs_context_multi_level(self):
        dummy_session = create_test_session([RolesConstants.SRS_EXTRACTS])
        dummy_session.set_user_context([RoleRelation(RolesConstants.SRS_EXTRACTS, self.tenant, 'ES', None, None),
                                        RoleRelation(RolesConstants.SRS_EXTRACTS, self.tenant, None, None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            student_reg = connection.get_table(Constants.STUDENT_REG)
            query = select([student_reg.c.school_guid],
                           from_obj=([student_reg]))
            srs = SRSExtracts(connection, RolesConstants.SRS_EXTRACTS)
            clause = srs.get_context(self.tenant, self.user)
            self.assertEqual(len(clause), 1)
            query = query.where(*clause)
            result = connection.get_result(query)
            self.assertEqual(len(result), 2581)

    def test_has_srs_context_with_context(self):
        with UnittestEdcoreDBConnection() as connection:
            srs = SRSExtracts(connection, RolesConstants.SRS_EXTRACTS)
            context = srs.check_context(self.tenant, self.user, ['115f7b10-9e18-11e2-9e96-0800200c9a66'])
            self.assertTrue(context)

    def test_has_srs_context_with_no_context(self):
        with UnittestEdcoreDBConnection() as connection:
            srs = SRSExtracts(connection, RolesConstants.SRS_EXTRACTS)
            context = srs.check_context(self.tenant, self.user, ['notyourstudent'])
            self.assertFalse(context)

    def test_has_srs_context_with_some_invalid_guids(self):
        with UnittestEdcoreDBConnection() as connection:
            srs = SRSExtracts(connection, RolesConstants.SRS_EXTRACTS)
            context = srs.check_context(self.tenant, self.user, ['115f7b10-9e18-11e2-9e96-0800200c9a66', 'notyourstudent'])
            self.assertFalse(context)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
