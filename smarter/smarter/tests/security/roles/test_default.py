'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import select
from smarter.security.roles.default import append_context
from smarter.reports.helpers.constants import Constants


class TestDefaultContextSecurity(Unittest_with_smarter_sqlite):

    def test_append_context(self):
        with SmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.student_guid],
                           from_obj=([fact_asmt_outcome]))
            results = connection.get_result(query)

            context_query = append_context(connection, query, '123')
            context_results = connection.get_result(context_query)

            self.assertEqual(len(results), len(context_results))
            self.assertEqual(query, context_query)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
