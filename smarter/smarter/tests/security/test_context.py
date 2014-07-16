'''
Created on May 7, 2013

@author: dip
'''
import unittest

from pyramid import testing
from pyramid.testing import DummyRequest

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.security.context import check_context, select_with_context,\
    get_current_context

# Import the roles below so test can run as a standalone
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edcore.security.tenant import set_tenant_map
from smarter.reports.helpers.constants import Constants
from smarter_common.security.constants import RolesConstants
from sqlalchemy.sql.expression import and_
from edauth.security.user import RoleRelation
from smarter.security.roles.pii import PII  # @UnusedImport
from smarter.security.roles.state_level import StateLevel  # @UnusedImport


class TestContext(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()
        set_tenant_map({self.__tenant_name: "NC"})
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout')),
                         (Allow, RolesConstants.SRS_EXTRACTS, ('view', 'logout')),
                         (Allow, RolesConstants.SRC_EXTRACTS, ('view', 'logout')),
                         (Allow, RolesConstants.AUDIT_XML_EXTRACTS, ('view', 'logout')),
                         (Allow, RolesConstants.ITEM_LEVEL_EXTRACTS, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), "NC", "228", "242"),
                                        RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), "NC", "228", "245"),
                                        RoleRelation(RolesConstants.SRS_EXTRACTS, get_unittest_tenant_name(), 'NC', None, None),
                                        RoleRelation(RolesConstants.SRC_EXTRACTS, get_unittest_tenant_name(), 'NC', None, None),
                                        RoleRelation(RolesConstants.AUDIT_XML_EXTRACTS, get_unittest_tenant_name(), 'NC', None, None)])
        # For Context Security, we need to save the user object
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_select_with_context_as_pii(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select_with_context([fact_asmt_outcome_vw.c.school_guid],
                                        from_obj=([fact_asmt_outcome_vw]), limit=1, permission=RolesConstants.PII, state_code='NC')
            results = connection.get_result(query)
            self.assertEqual(len(results), 1)
            self.assertIn(results[0][Constants.SCHOOL_GUID], ['242', '245'])

    def test_select_with_context_as_srs(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select_with_context([fact_asmt_outcome_vw.c.state_code],
                                        from_obj=([fact_asmt_outcome_vw]), limit=1, permission=RolesConstants.SRS_EXTRACTS, state_code='NC')
            results = connection.get_result(query.where(fact_asmt_outcome_vw.c.district_guid == '228'))
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][Constants.STATE_CODE], 'NC')

    def test_select_with_context_as_src(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select_with_context([fact_asmt_outcome_vw.c.state_code],
                                        from_obj=([fact_asmt_outcome_vw]), limit=1, permission=RolesConstants.SRC_EXTRACTS, state_code='NC')
            results = connection.get_result(query.where(fact_asmt_outcome_vw.c.district_guid == '228'))
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][Constants.STATE_CODE], 'NC')

    def test_select_with_context_or_query(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select_with_context([fact_asmt_outcome_vw.c.state_code],
                                        from_obj=([fact_asmt_outcome_vw]), permission=RolesConstants.PII, state_code='NC')
            query = query.where(and_(fact_asmt_outcome_vw.c.school_guid == '242'))
            results = connection.get_result(query)
            self.assertEqual(len(results), 234)

    def test_check_context_with_empty_guids(self):
        context = check_context('base', 'NC', [])
        self.assertFalse(context)

    def test_check_context_with_context_as_pii(self):
        context = check_context(RolesConstants.PII, 'NC', ['8b315698-7436-40f3-8cc1-28d4734b57e1'])
        self.assertTrue(context)

    def test_check_context_with_context_as_default(self):
        context = check_context('base', 'NC', ['8b315698-7436-40f3-8cc1-28d4734b57e1'])
        self.assertTrue(context)

    def test_get_current_context_at_state_level(self):
        context = get_current_context({'stateCode': 'NC'})
        self.assertTrue(context['pii']['all'])
        self.assertFalse(context['sar_extracts']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])

    def test_get_current_context_at_state_level_with_invalid_state(self):
        context = get_current_context({'stateCode': 'AA'})
        self.assertTrue(context['pii']['all'])
        self.assertFalse(context['sar_extracts']['all'])
        self.assertFalse(context['srs_extracts']['all'])
        self.assertFalse(context['src_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])
        self.assertFalse(context['audit_xml_extracts']['all'])

    def test_get_current_context_at_district_level(self):
        context = get_current_context({'stateCode': 'NC', 'districtGuid': '228'})
        self.assertTrue(context['pii']['all'])
        self.assertFalse(context['sar_extracts']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])

    def test_get_current_context_at_district_level_with_invalid_district(self):
        context = get_current_context({'stateCode': 'NC', 'districtGuid': '229'})
        self.assertTrue(context['pii']['all'])
        self.assertFalse(context['sar_extracts']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])

    def test_get_current_context_at_school_level(self):
        context = get_current_context({'stateCode': 'NC', 'districtGuid': '228', 'schoolGuid': '242'})
        self.assertTrue(context['pii']['all'])
        self.assertFalse(context['sar_extracts']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])

    def test_get_current_context_at_school_level_with_invalid_school(self):
        context = get_current_context({'stateCode': 'NC', 'districtGuid': '229', 'schoolGuid': 'bad'})
        self.assertFalse(context['pii']['all'])
        self.assertFalse(context['sar_extracts']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])

    def test_consortium_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, None, None, None, None),
                                        RoleRelation(RolesConstants.SRS_EXTRACTS, None, None, None, None),
                                        RoleRelation(RolesConstants.SRC_EXTRACTS, None, None, None, None),
                                        RoleRelation(RolesConstants.AUDIT_XML_EXTRACTS, None, None, None, None)])
        # For Context Security, we need to save the user object
        self.__config.testing_securitypolicy(dummy_session.get_user())
        context = get_current_context({'stateCode': 'NC', 'districtGuid': '229', 'schoolGuid': '242'})
        self.assertTrue(context['pii']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertFalse(context['item_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])

    def test_state_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', None, None),
                                        RoleRelation(RolesConstants.SRS_EXTRACTS, get_unittest_tenant_name(), 'NC', None, None),
                                        RoleRelation(RolesConstants.SRC_EXTRACTS, get_unittest_tenant_name(), 'NC', None, None),
                                        RoleRelation(RolesConstants.AUDIT_XML_EXTRACTS, None, None, None, None)])
        # For Context Security, we need to save the user object
        self.__config.testing_securitypolicy(dummy_session.get_user())
        context = get_current_context({'stateCode': 'NC', 'districtGuid': '229', 'schoolGuid': '242'})
        self.assertTrue(context['pii']['all'])
        self.assertTrue(context['srs_extracts']['all'])
        self.assertTrue(context['src_extracts']['all'])
        self.assertTrue(context['audit_xml_extracts']['all'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
