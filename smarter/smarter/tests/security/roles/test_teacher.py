'''
Created on May 9, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from sqlalchemy.sql.expression import select
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.teacher import Teacher
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from edcore.security.tenant import set_tenant_map
from pyramid import testing
from pyramid.testing import DummyRequest
from pyramid.security import Allow
import edauth


class TestTeacherContextSecurity(Unittest_with_edcore_sqlite):

    def setUp(self):
        defined_roles = [(Allow, 'TEACHER', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        self.tenant = get_unittest_tenant_name()
        set_tenant_map({self.tenant: "NC"})
        dummy_session = create_test_session(['TEACHER'])
        dummy_session.set_user_context([RoleRelation("TEACHER", get_unittest_tenant_name(), "NC", "228", "242")])
        self.user = dummy_session.get_user()
        self.__request = DummyRequest()
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        self.__config.testing_securitypolicy(self.user)

    def test_append_teacher_context(self):
        with UnittestEdcoreDBConnection() as connection:
            teacher = Teacher(connection)
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.section_guid],
                           from_obj=([fact_asmt_outcome]))
            clause = teacher.get_context(self.tenant, self.user)

            results = connection.get_result(query.where(clause))
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.SECTION_GUID], '345')

    def test_check_context_with_context(self):
        with UnittestEdcoreDBConnection() as connection:
            teacher = Teacher(connection)
            student_guids = ['e2f3c6a5-e28b-43e8-817b-fc7afed02b9b']

            context = teacher.check_context(self.tenant, self.user, student_guids)
            self.assertTrue(context)

    def test_check_context_with_no_context(self):
        with UnittestEdcoreDBConnection() as connection:
            teacher = Teacher(connection)
            student_guids = ['dd']

            context = teacher.check_context(self.tenant, self.user, student_guids)
            self.assertFalse(context)

    def test_check_context_with_no_context_to_all_guids(self):
        with UnittestEdcoreDBConnection() as connection:
            teacher = Teacher(connection)
            student_guids = ['dd', 'e2f3c6a5-e28b-43e8-817b-fc7afed02b9b']

            context = teacher.check_context(self.tenant, self.user, student_guids)
            self.assertFalse(context)

    def test_check_context_with_empty_context(self):
        with UnittestEdcoreDBConnection() as connection:
            teacher = Teacher(connection)
            student_guids = []

            context = teacher.check_context(self.tenant, self.user, student_guids)
            self.assertTrue(context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
