'''
Created on May 9, 2013

@author: dip
'''
import unittest

from sqlalchemy.sql.expression import select, or_
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.security import Allow

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.pii import PII
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from edcore.security.tenant import set_tenant_map
import edauth
from smarter_common.security.constants import RolesConstants


class TestPIIContextSecurity(Unittest_with_edcore_sqlite):

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

    def test_pii_tenant_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), None, None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            clause = pii.get_context(self.tenant, self.user)
            self.assertEqual(len(clause), 0)

    def test_pii_state_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.state_code],
                           from_obj=([fact_asmt_outcome_vw])).where(fact_asmt_outcome_vw.c.rec_status == 'C')
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(*clause))
            self.assertEqual(len(results), 1161)

    def test_pii_district_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', '228', None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.state_code],
                           from_obj=([fact_asmt_outcome_vw]))
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(*clause))
            self.assertEqual(len(results), 340)

    def test_pii_school_level(self):
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.school_guid],
                           from_obj=([fact_asmt_outcome_vw]))
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(*clause))
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.SCHOOL_GUID], '242')

    def test_pii_context_with_multiple_chain(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', '228', '242'),
                                        RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', '229', None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.state_code],
                           from_obj=([fact_asmt_outcome_vw]))
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(or_(*clause)))
            self.assertEqual(len(results), 366)

    def test_pii_context_with_multiple_level_chain(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', '228', '242'),
                                        RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), 'NC', '228', '245')])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.state_code],
                           from_obj=([fact_asmt_outcome_vw]))
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(or_(*clause)))
            self.assertEqual(len(results), 274)

    def test_sar_extract_tenant_level(self):
        dummy_session = create_test_session([RolesConstants.SAR_EXTRACTS])
        dummy_session.set_user_context([RoleRelation(RolesConstants.SAR_EXTRACTS, get_unittest_tenant_name(), None, None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.SAR_EXTRACTS)
            clause = pii.get_context(self.tenant, self.user)
            self.assertEqual(len(clause), 0)

    def test_sar_extracts_state_level(self):
        dummy_session = create_test_session([RolesConstants.SAR_EXTRACTS])
        dummy_session.set_user_context([RoleRelation(RolesConstants.SAR_EXTRACTS, get_unittest_tenant_name(), 'NC', None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.SAR_EXTRACTS)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.state_code],
                           from_obj=([fact_asmt_outcome_vw])).where(fact_asmt_outcome_vw.c.rec_status == 'C')
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(*clause))
            self.assertEqual(len(results), 1161)

    def test_sar_extracts_district_level(self):
        dummy_session = create_test_session([RolesConstants.SAR_EXTRACTS])
        dummy_session.set_user_context([RoleRelation(RolesConstants.SAR_EXTRACTS, get_unittest_tenant_name(), 'NC', '228', None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.SAR_EXTRACTS)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.state_code],
                           from_obj=([fact_asmt_outcome_vw]))
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(*clause))
            self.assertEqual(len(results), 340)

    def test_sar_extracts_school_level(self):
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.SAR_EXTRACTS)
            fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact_asmt_outcome_vw.c.school_guid],
                           from_obj=([fact_asmt_outcome_vw]))
            clause = pii.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(*clause))
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.SCHOOL_GUID], '242')

    def test_check_context_with_context(self):
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            student_guids = ['e2f3c6a5-e28b-43e8-817b-fc7afed02b9b']

            context = pii.check_context(self.tenant, self.user, student_guids)
            self.assertTrue(context)

    def test_check_context_with_no_context(self):
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            student_guids = ['dd']

            context = pii.check_context(self.tenant, self.user, student_guids)
            self.assertFalse(context)

    def test_check_context_with_no_context_to_all_guids(self):
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            student_guids = ['dd', 'e2f3c6a5-e28b-43e8-817b-fc7afed02b9b']

            context = pii.check_context(self.tenant, self.user, student_guids)
            self.assertFalse(context)

    def test_check_context_with_empty_context(self):
        with UnittestEdcoreDBConnection() as connection:
            pii = PII(connection, RolesConstants.PII)
            student_guids = []

            context = pii.check_context(self.tenant, self.user, student_guids)
            self.assertTrue(context)

    def test_add_context_without_tenant(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, None, None, None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)

        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact.c.state_code], from_obj=[fact])
            pii = PII(connection, RolesConstants.PII)
            query = pii.add_context(self.tenant, self.user, query)
            result = connection.get_result(query)
            self.assertEqual(1221, len(result))

    def test_add_context_with_tenant(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, self.tenant, None, None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)

        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact.c.state_code], from_obj=[fact])
            pii = PII(connection, RolesConstants.PII)
            query = pii.add_context(get_unittest_tenant_name(), self.user, query)
            result = connection.get_result(query)
            self.assertEqual(1221, len(result))

    def test_add_context_with_state_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, self.tenant, 'NC', None, None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        # Checks that the query has applied where clause
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact.c.student_guid], from_obj=[fact])
            pii = PII(connection, RolesConstants.PII)
            query = pii.add_context(get_unittest_tenant_name(), self.user, query)
            self.assertIsNotNone(query._whereclause)
            result = connection.get_result(query)
            self.assertEqual(len(result), 1221)

    def test_add_context_with_district_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, self.tenant, 'NC', '228', None)])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        # Checks that the query has applied where clause
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact.c.state_code], from_obj=[fact])
            pii = PII(connection, RolesConstants.PII)
            query = pii.add_context(get_unittest_tenant_name(), self.user, query)
            result = connection.get_result(query)
            self.assertEqual(340, len(result))

    def test_add_context_with_school_level(self):
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, self.tenant, 'NC', '228', '242')])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)
        # Checks that the query has applied where clause
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            query = select([fact.c.state_code], from_obj=[fact])
            pii = PII(connection, RolesConstants.PII)
            query = pii.add_context(get_unittest_tenant_name(), self.user, query)
            result = connection.get_result(query)
            self.assertEqual(234, len(result))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
