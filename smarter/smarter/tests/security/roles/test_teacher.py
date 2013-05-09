'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import select
from smarter.security.roles.teacher import append_teacher_context,\
    get_teacher_context
from smarter.reports.helpers.constants import Constants


class TestTeacherContextSecurity(Unittest_with_smarter_sqlite):

    def test_get_teacher_context(self):
        guid = "272"
        with SmarterDBConnection() as connection:
            context = get_teacher_context(connection, guid)
            self.assertListEqual(context, ['345'])

    def test_get_teacher_context_invalid_guid(self):
        guid = "invalid-guid"
        with SmarterDBConnection() as connection:
            context = get_teacher_context(connection, guid)
            self.assertListEqual(context, [])

    def test_append_teacher_context(self):
        with SmarterDBConnection() as connection:
            guid = '963'
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.section_guid],
                           from_obj=([fact_asmt_outcome]))
            query = append_teacher_context(connection, query, guid)

            results = connection.get_result(query)
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.SECTION_GUID], '974')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
