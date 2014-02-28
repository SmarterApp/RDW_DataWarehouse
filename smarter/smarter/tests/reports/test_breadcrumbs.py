'''
Created on Mar 8, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from beaker.util import parse_cache_config_options
from edauth.tests.test_helper.create_session import create_test_session


class TestContext(Unittest_with_edcore_sqlite):
    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
        dummy_session = create_test_session(['TEACHER'], uid='272')
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def testStateContext(self):
        results = get_breadcrumbs_context(state_code='NC')
        self.assertEqual(len(results['items']), 2)
        self.assertEqual(results['items'][0]['name'], 'Home')
        self.assertEqual(results['items'][0]['type'], 'home')
        self.assertEqual(results['items'][1]['name'], 'North Carolina')
        self.assertEqual(results['items'][1]['id'], 'NC')
        self.assertEqual(results['items'][1]['type'], 'state')

    def testDistrictContext(self):
        results = get_breadcrumbs_context(state_code='NC', district_guid='228')
        self.assertEqual(len(results['items']), 3)
        self.assertEqual(results['items'][1]['name'], 'North Carolina')
        self.assertEqual(results['items'][1]['type'], 'state')
        self.assertEqual(results['items'][2]['name'], 'Sunset School District')
        self.assertEqual(results['items'][2]['type'], 'district')
        self.assertEqual(results['items'][2]['id'], '228')

    def testSchoolContext(self):
        results = get_breadcrumbs_context(state_code='NC', district_guid='228', school_guid='242')
        self.assertEqual(len(results['items']), 4)
        self.assertEqual(results['items'][1]['name'], 'North Carolina')
        self.assertEqual(results['items'][2]['name'], 'Sunset School District')
        self.assertEqual(results['items'][3]['name'], 'Sunset - Eastern Elementary')
        self.assertEqual(results['items'][3]['id'], '242')
        self.assertEqual(results['items'][3]['type'], 'school')

    def testGradeContext(self):
        results = get_breadcrumbs_context(state_code='NC', district_guid='228', school_guid='242', asmt_grade='3')
        self.assertEqual(len(results['items']), 5)
        self.assertEqual(results['items'][4]['name'], '3')
        self.assertEqual(results['items'][4]['id'], '3')
        self.assertEqual(results['items'][4]['type'], 'grade')

    def testStudentContext(self):
        results = get_breadcrumbs_context(state_code='NC', district_guid='228', school_guid='242', asmt_grade='3', student_name='StudentName')
        self.assertEqual(len(results['items']), 6)
        self.assertEqual(results['items'][5]['name'], 'StudentName')
        self.assertEqual(results['items'][5]['type'], 'student')

    def test_No_state_code(self):
        results = get_breadcrumbs_context()
        self.assertEqual(len(results['items']), 1)
        self.assertEqual(results['items'][0]['name'], 'Home')
        self.assertEqual(results['items'][0]['type'], 'home')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
