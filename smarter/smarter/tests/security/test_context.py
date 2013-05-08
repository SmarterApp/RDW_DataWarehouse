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
    append_student_context
from sqlalchemy.sql.expression import Select


class TestContext(Unittest_with_smarter_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_select_with_context_as_teacher(self):
        # TODO
        pass

    def test_get_teacher_context(self):
        guid = "272"
        with SmarterDBConnection() as connector:
            context = get_teacher_context(connector, guid)
            self.assertListEqual(context, ['345'])

    def test_get_student_context(self):
        guid = "a016a4c1-5aca-4146-a85b-ed1172a01a4d"
        with SmarterDBConnection() as connector:
            context = get_student_context(connector, guid)
            self.assertListEqual(context, [guid])

    def test_append_teacher_context(self):
        with SmarterDBConnection() as connector:
            guid = '963'
            fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
            query = Select([fact_asmt_outcome.c.section_guid],
                           from_obj=([fact_asmt_outcome]))
            query = append_teacher_context(connector, query, guid)

            results = connector.get_result(query)
            for result in results:
                self.assertEqual(result['section_guid'], '974')

    def test_append_student_context(self):
        with SmarterDBConnection() as connector:
            guid = '61ec47de-e8b5-4e78-9beb-677c44dd9b50'
            fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
            query = Select([fact_asmt_outcome.c.student_guid],
                           from_obj=([fact_asmt_outcome]))
            query = append_student_context(connector, query, guid)

            results = connector.get_result(query)
            for result in results:
                self.assertEqual(result['student_guid'], '61ec47de-e8b5-4e78-9beb-677c44dd9b50')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
