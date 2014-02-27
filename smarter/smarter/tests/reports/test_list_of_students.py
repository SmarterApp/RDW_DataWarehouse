'''
Created on Feb 4, 2013

@author: tosako
'''
import unittest
from smarter.reports.list_of_students_report import get_list_of_students_report
from edapi.exceptions import NotFoundException
from pyramid.testing import DummyRequest
from pyramid import testing
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection
from edauth.tests.test_helper.create_session import create_test_session


class TestLOS(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }

        CacheManager(**parse_cache_config_options(cache_opts))

        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        # Set up context security
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

    def test_assessments(self):
        testParam = {}
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('cutpoints' in results['metadata'], "returning JSON must have metadata")
        self.assertTrue('assessments' in results, "returning JSON must have assessments")

        cutpoints = results['metadata']['cutpoints']
        self.assertEqual(2, len(cutpoints), "cutpoints are ELA and MATH")
        self.assertTrue('subject2' in cutpoints, 'subject2')
        self.assertTrue('subject1' in cutpoints, 'subject1')

        claims = results['metadata']['claims']
        self.assertEqual(2, len(claims), "cutpoints are ELA and MATH")
        self.assertTrue('subject2' in claims)
        self.assertTrue('subject1' in claims)

        assessments = results['assessments']
        self.assertEqual(35, len(assessments), "35 assessments")
        self.assertEqual("Verda", assessments[9]['student_first_name'], "student_first_name")
        self.assertEqual("Lettie", assessments[10]['student_first_name'], "student_first_name")
        self.assertEqual("Mi-Ha", assessments[29]['student_first_name'], "student_first_name")

    def test_breadcrumbs(self):
        testParam = {}
        testParam['stateCode'] = 'NC'
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('context' in results, "returning JSON must have context")

    def test_asmt_administration(self):
        testParam = {}
        testParam['stateCode'] = 'NC'
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['asmtSubject'] = ['ELA', 'Math']
        results = get_list_of_students_report(testParam)
        self.assertTrue('asmt_administration' in results, "asmt_administration is missing")
        self.assertEquals(len(results['asmt_administration']), 2, "should have 2 different test")

    def test_ELA_only(self):
        testParam = {}
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['ELA']
        results = get_list_of_students_report(testParam)

        self.assertTrue('metadata' in results, "returning JSON must have metadata")
        self.assertTrue('assessments' in results, "returning JSON must have assessments")

        cutpoints = results['metadata']['cutpoints']
        self.assertEqual(1, len(cutpoints), "cutpoints are ELA and MATH")
        self.assertTrue('subject1' in cutpoints, 'subject1')

        claims = results['metadata']['claims']
        self.assertEqual(1, len(claims), "claims are ELA")
        self.assertTrue('subject1' in claims, 'subject1')

    def test_Math_only(self):
        testParam = {}
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = '3'
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['Math']
        results = get_list_of_students_report(testParam)

        self.assertTrue('metadata' in results, "returning JSON must have cutpoints")

        cutpoints = results['metadata']['cutpoints']
        self.assertEqual(1, len(cutpoints))
        self.assertTrue('subject1' in cutpoints, 'subject1')

        claims = results['metadata']['claims']
        self.assertEqual(1, len(claims), "claims are ELA")
        self.assertTrue('subject1' in claims, 'subject1')

    def test_invalid_asmt_subject(self):
        testParam = {}
        testParam['districtGuid'] = '228'
        testParam['schoolGuid'] = '242'
        testParam['asmtGrade'] = 3
        testParam['stateCode'] = 'NC'
        testParam['asmtSubject'] = ['Dummy']
        self.assertRaises(NotFoundException, get_list_of_students_report, testParam)

    def test_LOS_with_filters(self):
        testParam = {'asmtGrade': '3', 'gender': ['male'], 'stateCode': 'NC', 'districtGuid': '228', 'schoolGuid': '242'}
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 17)

        testParam['gender'] = ['not_stated']
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 0)

    def test_asmt_type(self):
        testParam = {'asmtGrade': '3', 'stateCode': 'NC', 'districtGuid': '228', 'schoolGuid': '242'}
        results = get_list_of_students_report(testParam)
        self.assertEqual(len(results['assessments']), 35)
        self.assertIsNotNone(results['assessments'][0]['Interim Comprehensive']['subject1'])
        self.assertIsNotNone(results['assessments'][0]['Summative']['subject1'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
