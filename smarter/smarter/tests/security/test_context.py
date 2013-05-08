'''
Created on May 7, 2013

@author: dip
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from pyramid import testing
from pyramid.testing import DummyRequest
from smarter.database.connector import SmarterDBConnection
from smarter.security.context import get_teacher_context,\
    get_student_context, append_teacher_context,\
    append_student_context, select_with_context
from sqlalchemy.sql.expression import select
from edauth.security.user import User


class TestContext(Unittest_with_smarter_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with SmarterDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_select_with_context_as_teacher_with_no_user_mapping(self):
        dummy_user = User()
        dummy_user.set_roles(['TEACHER'])
        dummy_user.set_uid('272')
        self.__config.testing_securitypolicy(dummy_user)
        with SmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            query = select_with_context([fact_asmt_outcome.c.section_guid],
                                        from_obj=([fact_asmt_outcome]))
            results = connection.get_result(query)
            self.assertListEqual([], results)

    def test_select_with_context_as_teacher(self):
        dummy_user = User()
        dummy_user.set_roles(['TEACHER'])
        dummy_user.set_uid('272')
        self.__config.testing_securitypolicy(dummy_user)
        with SmarterDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', staff_guid='272')

            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            query = select_with_context([fact_asmt_outcome.c.section_guid],
                                        from_obj=([fact_asmt_outcome]))
            results = connection.get_result(query)
            for result in results:
                self.assertEquals(result['section_guid'], '345')

    def test_select_with_context_as_student(self):
        uid = "61ec47de-e8b5-4e78-9beb-677c44dd9b50"
        dummy_user = User()
        dummy_user.set_roles(['STUDENT'])
        dummy_user.set_uid(uid)
        self.__config.testing_securitypolicy(dummy_user)
        with SmarterDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id=uid, staff_guid=uid)

            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            query = select_with_context([fact_asmt_outcome.c.student_guid],
                                        from_obj=([fact_asmt_outcome]))
            results = connection.get_result(query)
            for result in results:
                self.assertEquals(result['student_guid'], uid)

    def test_get_teacher_context(self):
        guid = "272"
        with SmarterDBConnection() as connection:
            context = get_teacher_context(connection, guid)
            self.assertListEqual(context, ['345'])

    def test_get_student_context(self):
        guid = "a016a4c1-5aca-4146-a85b-ed1172a01a4d"
        with SmarterDBConnection() as connection:
            context = get_student_context(connection, guid)
            self.assertListEqual(context, [guid])

    def test_append_teacher_context(self):
        with SmarterDBConnection() as connection:
            guid = '963'
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            query = select([fact_asmt_outcome.c.section_guid],
                           from_obj=([fact_asmt_outcome]))
            query = append_teacher_context(connection, query, guid)

            results = connection.get_result(query)
            for result in results:
                self.assertEqual(result['section_guid'], '974')

    def test_append_student_context(self):
        with SmarterDBConnection() as connection:
            guid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            query = select([fact_asmt_outcome.c.student_guid],
                           from_obj=([fact_asmt_outcome]))
            query = append_student_context(connection, query, guid)

            results = connection.get_result(query)
            for result in results:
                self.assertEqual(result['student_guid'], '61ec47de-e8b5-4e78-9beb-677c44dd9b50')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
