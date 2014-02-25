'''
Created on May 7, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from pyramid import testing
from pyramid.testing import DummyRequest
from smarter.security.context import select_with_context, check_context
from edapi.exceptions import ForbiddenError
from smarter.security.constants import RolesConstants
from smarter.reports.helpers.constants import Constants
from edauth.security.session import Session
# Import the roles below so test can run as a standalone
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.student import Student  # @UnusedImport


class TestContext(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table(Constants.USER_MAPPING)
            connection.execute(user_mapping.delete())

#    def test_select_with_context_as_teacher_with_no_user_mapping(self):
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.TEACHER])
#        dummy_session.set_uid('272')
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
#            self.assertRaises(ForbiddenError, select_with_context, [fact_asmt_outcome.c.section_guid], from_obj=([fact_asmt_outcome]))

#    def test_select_with_context_as_teacher(self):
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.TEACHER])
#        dummy_session.set_uid('272')
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            # Insert into user_mapping table
#            user_mapping = connection.get_table(Constants.USER_MAPPING)
#            connection.execute(user_mapping.insert(), user_id='272', guid='272')
#
#            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
#            query = select_with_context([fact_asmt_outcome.c.section_guid],
#                                        from_obj=([fact_asmt_outcome]))
#            results = connection.get_result(query)
#            for result in results:
#                self.assertEquals(result[Constants.SECTION_GUID], '345')

    def test_select_with_context_as_student(self):
        uid = "61ec47de-e8b5-4e78-9beb-677c44dd9b50"
        dummy_session = Session()
        dummy_session.set_roles([RolesConstants.STUDENT])
        dummy_session.set_uid(uid)
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table(Constants.USER_MAPPING)
            connection.execute(user_mapping.insert(), user_id=uid, guid=uid)

            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select_with_context([fact_asmt_outcome.c.student_guid],
                                        from_obj=([fact_asmt_outcome]))
            results = connection.get_result(query)
            for result in results:
                self.assertEquals(result[Constants.STUDENT_GUID], uid)

#    def test_select_with_context_as_school_admin_one(self):
#        uid = "951"
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_1])
#        dummy_session.set_uid(uid)
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            # Insert into user_mapping table
#            user_mapping = connection.get_table(Constants.USER_MAPPING)
#            connection.execute(user_mapping.insert(), user_id=uid, guid=uid)
#
#            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
#            query = select_with_context([fact_asmt_outcome.c.school_guid],
#                                        from_obj=([fact_asmt_outcome]))
#            results = connection.get_result(query)
#            for result in results:
#                self.assertEquals(result[Constants.SCHOOL_GUID], '229')

#    def test_select_with_context_as_school_admin_two(self):
#        uid = "270"
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_2])
#        dummy_session.set_uid(uid)
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            # Insert into user_mapping table
#            user_mapping = connection.get_table(Constants.USER_MAPPING)
#            connection.execute(user_mapping.insert(), user_id=uid, guid=uid)
#
#            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
#            query = select_with_context([fact_asmt_outcome.c.school_guid],
#                                        from_obj=([fact_asmt_outcome]))
#            results = connection.get_result(query)
#            for result in results:
#                self.assertEquals(result[Constants.SCHOOL_GUID], '242')

    def test_select_with_context_with_multi_roles(self):
        pass

    def test_check_context_with_empty_guids(self):
        context = check_context('NC', [])
        self.assertFalse(context)

#    def test_check_context_with_context_as_teacher(self):
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.TEACHER])
#        dummy_session.set_uid('272')
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            # Insert into user_mapping table
#            user_mapping = connection.get_table(Constants.USER_MAPPING)
#            connection.execute(user_mapping.insert(), user_id='272', guid='272')
#
#        context = check_context(['8b315698-7436-40f3-8cc1-28d4734b57e1'])
#        self.assertTrue(context)

    def test_check_context_as_student(self):
        uid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
        dummy_session = Session()
        dummy_session.set_roles([RolesConstants.STUDENT])
        dummy_session.set_uid(uid)
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table(Constants.USER_MAPPING)
            connection.execute(user_mapping.insert(), user_id=uid, guid=uid)

        context = check_context('NC', ['61ec47de-e8b5-4e78-9beb-677c44dd9b50'])
        self.assertTrue(context)

#    def test_check_context_as_school_admin_with_no_context(self):
#        uid = "273"
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_1])
#        dummy_session.set_uid(uid)
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            # Insert into user_mapping table
#            user_mapping = connection.get_table(Constants.USER_MAPPING)
#            connection.execute(user_mapping.insert(), user_id=uid, guid=uid)
#
#        context = check_context(['c95bbd44-bc4e-4441-a451-8f0b6aec8c37'])
#        self.assertFalse(context)

#    def test_check_context_as_school_admin_two_with_no_context(self):
#        uid = "273"
#        dummy_session = Session()
#        dummy_session.set_roles([RolesConstants.SCHOOL_EDUCATION_ADMINISTRATOR_2])
#        dummy_session.set_uid(uid)
#        dummy_session.set_tenants(self.__tenant_name)
#        self.__config.testing_securitypolicy(dummy_session)
#        with UnittestEdcoreDBConnection() as connection:
#            # Insert into user_mapping table
#            user_mapping = connection.get_table(Constants.USER_MAPPING)
#            connection.execute(user_mapping.insert(), user_id=uid, guid=uid)
#
#        context = check_context(['61ec47de-e8b5-4e78-9beb-677c44dd9b50', '34140997-8949-497e-bbbb-5d72aa7dc9cb'])
#        self.assertTrue(context)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
