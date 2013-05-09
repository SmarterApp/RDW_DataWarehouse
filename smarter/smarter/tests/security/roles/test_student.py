'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import select
from smarter.security.roles.student import append_student_context,\
    get_student_context
from smarter.reports.helpers.constants import Constants


class TestStudentContextSecurity(Unittest_with_smarter_sqlite):

    def test_get_student_context(self):
        guid = "a016a4c1-5aca-4146-a85b-ed1172a01a4d"
        with SmarterDBConnection() as connection:
            context = get_student_context(connection, guid)
            self.assertListEqual(context, [guid])

    def test_get_school_admin_invalid_guid(self):
        guid = "invalid-guid"
        with SmarterDBConnection() as connection:
            context = get_student_context(connection, guid)
            self.assertListEqual(context, [])

    def test_append_student_context(self):
        with SmarterDBConnection() as connection:
            guid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.student_guid],
                           from_obj=([fact_asmt_outcome]))
            query = append_student_context(connection, query, guid)

            results = connection.get_result(query)
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.STUDENT_GUID], '61ec47de-e8b5-4e78-9beb-677c44dd9b50')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
