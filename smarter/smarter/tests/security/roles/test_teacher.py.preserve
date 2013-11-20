'''
Created on May 9, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection
from sqlalchemy.sql.expression import select
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.teacher import Teacher
from edapi.exceptions import ForbiddenError


class TestTeacherContextSecurity(Unittest_with_edcore_sqlite):

    def test_get_teacher_context_invalid_guid(self):
        guid = "invalid-guid"
        with UnittestEdcoreDBConnection() as connection:
            teacher = Teacher(connection)
            self.assertRaises(ForbiddenError, teacher.get_context, guid)

#    def test_append_teacher_context(self):
#        with UnittestEdcoreDBConnection() as connection:
#            guid = '963'
#            teacher = Teacher(connection)
#            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
#            query = select([fact_asmt_outcome.c.section_guid],
#                           from_obj=([fact_asmt_outcome]))
#            clause = teacher.get_context(guid)
#
#            results = connection.get_result(query.where(clause))
#            self.assertTrue(len(results) > 0)
#            for result in results:
#                self.assertEqual(result[Constants.SECTION_GUID], '974')
#
#    def test_check_context_with_context(self):
#        with UnittestEdcoreDBConnection() as connection:
#            guid = '963'
#            teacher = Teacher(connection)
#            student_guids = ['3efe8485-9c16-4381-ab78-692353104cce']
#
#            context = teacher.check_context(guid, student_guids)
#            self.assertTrue(context)
#
#    def test_check_context_with_no_context(self):
#        with UnittestEdcoreDBConnection() as connection:
#            guid = '963'
#            teacher = Teacher(connection)
#            student_guids = ['dd']
#
#            context = teacher.check_context(guid, student_guids)
#            self.assertFalse(context)
#
#    def test_check_context_with_no_context_to_all_guids(self):
#        with UnittestEdcoreDBConnection() as connection:
#            guid = '963'
#            teacher = Teacher(connection)
#            student_guids = ['dd', '3efe8485-9c16-4381-ab78-692353104cce']
#
#            context = teacher.check_context(guid, student_guids)
#            self.assertFalse(context)
#
#    def test_check_context_with_empty_context(self):
#        with UnittestEdcoreDBConnection() as connection:
#            guid = '963'
#            teacher = Teacher(connection)
#            student_guids = []
#
#            context = teacher.check_context(guid, student_guids)
#            self.assertTrue(context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
