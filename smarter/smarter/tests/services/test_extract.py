'''
Created on Nov 8, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from pyramid.registry import Registry
from edauth.security.session import Session
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from edextract.celery import setup_celery
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from pyramid.response import Response
from smarter.extracts.constants import Constants
from smarter.services.extract import post_extract_service, get_extract_service,\
    generate_zip_file_name
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
import smarter.extracts.format
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class TestExtract(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        reg.settings = {}
        reg.settings['extract.available_grades'] = '3,4,5,6,7,8,9,11'
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='1023', guid='1023')
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        # celery settings for UT
        settings = {'extract.celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)
        # for UT purposes
        smarter.extracts.format.json_column_mapping = {}

    def tearDown(self):
        self.__request = None
        testing.tearDown()
        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_post_valid_response_tenant_extract(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['CA'],
                                    'asmtYear': ['2015'],
                                    'asmtType': ['SUMMATIVE'],
                                    'asmtSubject': ['Math'],
                                    'extractType': ['studentAssessment'],
                                    'async': 'true'}
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        results = post_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        self.assertEqual(len(results.json_body['tasks']), 1)
        self.assertEqual(results.json_body['tasks'][0][Constants.STATUS], Constants.FAIL)

    def test_get_invalid_param_tenant_extract(self):
        self.__request.GET['stateCode'] = 'NY'
        self.__request.GET['asmyType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_extract_service)

    def test_post_valid_response_failed_task_tenant_extract(self):
        self.__request.GET['stateCode'] = 'NY'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2010'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        results = get_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.FAIL)

    def test_multi_tasks_tenant_extract(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['CA'],
                                    'asmtYear': ['2015', '2011'],
                                    'asmtType': ['SUMMATIVE'],
                                    'asmtSubject': ['Math', 'ELA'],
                                    'extractType': ['studentAssessment'],
                                    'async': 'true'}
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        results = post_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.FAIL)
        self.assertEqual(tasks[1][Constants.STATUS], Constants.FAIL)

    def test_generate_zip_file_name_for_grades(self):
        params = {'asmtGrade': '6',
                  'asmtSubject': ['Math'],
                  'asmtType': 'SUMMATIVE',
                  'stateCode': 'NY'}
        name = generate_zip_file_name(params)
        self.assertIn('ASMT_GRADE_6_MATH_SUMMATIVE', name)

    def test_generate_zip_file_name_for_schools(self):
        params = {'asmtSubject': ['Math', 'ELA'],
                  'asmtType': 'Summative',
                  'stateCode': 'NY'}
        name = generate_zip_file_name(params)
        self.assertIn('ASMT_ELA_MATH_SUMMATIVE', name)

    def test_post_invalid_payload(self):
        self.assertRaises(EdApiHTTPPreconditionFailed, post_extract_service)

    def test_post_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, post_extract_service, self.__request)

    def test_get_invalid_param(self):
        self.__request.GET['stateCode'] = 'NY'
        self.__request.GET['asmtSubject'] = ['MATH']
        self.__request.GET['asmyType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['districtGuid'] = '203'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_extract_service)

    def test_get_extract_service(self):
        self.__request.GET['stateCode'] = 'NY'
        self.__request.GET['districtGuid'] = '229'
        self.__request.GET['schoolGuid'] = '936'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        response = get_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_post_extract_service(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NY'],
                                    'districtGuid': '229',
                                    'schoolGuid': '936',
                                    'asmtSubject': ['Math'],
                                    'asmtType': ['SUMMATIVE']}
        response = post_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_get_valid_tenant_extract(self):
        self.__request.GET['stateCode'] = 'NY'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2015'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        results = get_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.OK)

    def test_post_valid_tenant_extract(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NY'],
                                    'asmtSubject': ['Math'],
                                    'asmtType': ['SUMMATIVE'],
                                    'asmtYear': ['2015'],
                                    'extractType': ['studentAssessment'],
                                    'async': 'true'}
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        response = post_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/json')
        tasks = response.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.OK)

    def test_with_no_sync_or_async_set(self):
        self.__request.GET['stateCode'] = 'NY'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2015'
        self.__request.GET['extractType'] = 'studentAssessment'
        dummy_session = Session()
        dummy_session.set_roles(['SCHOOL_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('1023')
        dummy_session.set_tenant(self.__tenant_name)
        self.__config.testing_securitypolicy(dummy_session)
        response = get_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
