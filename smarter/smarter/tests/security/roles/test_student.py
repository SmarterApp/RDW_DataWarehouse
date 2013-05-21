'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import select
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.student import Student


class TestStudentContextSecurity(Unittest_with_smarter_sqlite):

    def test_get_student_invalid_guid(self):
        with SmarterDBConnection() as connection:
            guid = "invalid-guid"
            student_context = Student(connection)

            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.student_guid],
                           from_obj=([fact_asmt_outcome]))
            clause = student_context.get_context(guid)

            results = connection.get_result(query.where(clause))
            self.assertEqual(len(results), 0)

    def test_get_student_context(self):
        with SmarterDBConnection() as connection:
            guid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'

            student_context = Student(connection)

            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.student_guid],
                           from_obj=([fact_asmt_outcome]))
            clause = student_context.get_context(guid)

            results = connection.get_result(query.where(clause))
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.STUDENT_GUID], '61ec47de-e8b5-4e78-9beb-677c44dd9b50')

    def test_check_context(self):
        guid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
        student = Student('conn')

        context = student.check_context(guid, [guid])
        self.assertTrue(context)

    def test_check_context_with_no_context(self):
        guid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
        student = Student('conn')

        context = student.check_context(guid, [guid, 'a', 'b'])
        self.assertFalse(context)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
