'''
Created on May 9, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from smarter.database.connector import SmarterDBConnection
from sqlalchemy.sql.expression import select
from smarter.reports.helpers.constants import Constants
from smarter.security.roles.school_admin import SchoolAdmin
from edapi.exceptions import ForbiddenError


class TestSchoolAdminContextSecurity(Unittest_with_smarter_sqlite):

    def test_get_school_admin_invalid_guid(self):
        guid = "invalid-guid"
        with SmarterDBConnection() as connection:
            school_admin = SchoolAdmin(connection)
            self.assertRaises(ForbiddenError, school_admin.get_context, guid)

    def test_get_school_admin_context(self):
        with SmarterDBConnection() as connection:
            guid = '1023'
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            school_admin = SchoolAdmin(connection)
            clause = school_admin.get_context(guid)

            results = connection.get_result(query.where(clause))
            self.assertTrue(len(results) > 0)
            for result in results:
                self.assertEqual(result[Constants.SCHOOL_GUID], '939')

    def test_has_school_admin_context_with_context(self):
        with SmarterDBConnection() as connection:
            guid = '1023'
            school_admin = SchoolAdmin(connection)
            context = school_admin.check_context(guid, ['115f7b10-9e18-11e2-9e96-0800200c9a66'])
            self.assertTrue(context)

    def test_has_school_admin_context_with_no_context(self):
        with SmarterDBConnection() as connection:
            guid = '1023'
            school_admin = SchoolAdmin(connection)
            context = school_admin.check_context(guid, ['notyourstudent'])
            self.assertFalse(context)

    def test_has_school_school_context_with_some_invalid_guids(self):
        with SmarterDBConnection() as connection:
            guid = '1023'
            school_admin = SchoolAdmin(connection)
            context = school_admin.check_context(guid, ['115f7b10-9e18-11e2-9e96-0800200c9a66', 'notyourstudent'])
            self.assertFalse(context)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
