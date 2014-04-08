'''
Created on May 7, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from pyramid import testing
from pyramid.testing import DummyRequest
from smarter.security.context import check_context, select_with_context
# Import the roles below so test can run as a standalone
from smarter.security.roles.pii import PII  # @UnusedImport
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edcore.security.tenant import set_tenant_map
from smarter.reports.helpers.constants import Constants
from smarter.security.constants import RolesConstants
from sqlalchemy.sql.expression import and_
from edauth.security.user import RoleRelation


class TestContext(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()
        set_tenant_map({self.__tenant_name: "NC"})
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), "NC", "228", "242"),
                                        RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), "NC", "228", "245")])
        # For Context Security, we need to save the user object
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_select_with_context_as_pii(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select_with_context([fact_asmt_outcome.c.school_guid],
                                        from_obj=([fact_asmt_outcome]), limit=1, permission=RolesConstants.PII, state_code='NC')
            results = connection.get_result(query)
            self.assertEqual(len(results), 1)
            self.assertIn(results[0][Constants.SCHOOL_GUID], ['242', '245'])

    def test_select_with_context_or_query(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select_with_context([fact_asmt_outcome.c.state_code],
                                        from_obj=([fact_asmt_outcome]), permission=RolesConstants.PII, state_code='NC')
            query = query.where(and_(fact_asmt_outcome.c.school_guid == '242'))
            results = connection.get_result(query)
            self.assertEqual(len(results), 271)

    def test_check_context_with_empty_guids(self):
        context = check_context('base', 'NC', [])
        self.assertFalse(context)

    def test_check_context_with_context_as_pii(self):
        context = check_context(RolesConstants.PII, 'NC', ['8b315698-7436-40f3-8cc1-28d4734b57e1'])
        self.assertTrue(context)

    def test_check_context_with_context_as_default(self):
        context = check_context('base', 'NC', ['8b315698-7436-40f3-8cc1-28d4734b57e1'])
        self.assertTrue(context)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
