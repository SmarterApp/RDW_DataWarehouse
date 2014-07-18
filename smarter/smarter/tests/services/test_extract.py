'''
Created on Nov 8, 2013

@author: dip
'''
import unittest
import zipfile
import tempfile
from unittest.mock import patch

from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.registry import Registry
from pyramid.response import Response
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pyramid.security import Allow

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edextract.celery import setup_celery
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from smarter.extracts.constants import Constants
from smarter.services.extract import post_extract_service, get_extract_service,\
    generate_zip_file_name, send_extraction_request
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
import smarter.extracts.format
from edapi.utils import convert_query_string_to_dict_arrays
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from edcore.security.tenant import set_tenant_map
from smarter_common.security.constants import RolesConstants
from smarter.security.roles.pii import PII  # @UnusedImport
from smarter.reports.helpers.constants import Constants as ReportConstants


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
        reg.settings = {'extract.available_grades': '3,4,5,6,7,8,9,11',
                        'hpz.file_upload_base_url': 'http://somehost:82/files'}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()

        defined_roles = [(Allow, RolesConstants.SAR_EXTRACTS, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.SAR_EXTRACTS])
        self.__config.testing_securitypolicy(dummy_session.get_user())
        # celery settings for UT
        settings = {'extract.celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)
        # for UT purposes
        smarter.extracts.format.json_column_mapping = {}
        set_tenant_map({'tomcat': 'NC'})

    def tearDown(self):
        self.__request = None
        testing.tearDown()

    def test_post_valid_response_tenant_extract(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NC'],
                                    'asmtYear': ['2018'],
                                    'asmtType': ['SUMMATIVE'],
                                    'asmtSubject': ['Math'],
                                    'extractType': ['studentAssessment'],
                                    'async': 'true'}
        results = post_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        self.assertEqual(len(results.json_body['tasks']), 1)
        self.assertEqual(results.json_body['tasks'][0][Constants.STATUS], Constants.NO_DATA)

    def test_get_invalid_param_tenant_extract(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmyType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_extract_service)

    def test_post_valid_response_failed_task_tenant_extract(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2010'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        results = get_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.NO_DATA)

    def test_multi_tasks_tenant_extract(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NC'],
                                    'asmtYear': ['2019', '2011'],
                                    'asmtType': ['SUMMATIVE'],
                                    'asmtSubject': ['Math', 'ELA'],
                                    'extractType': ['studentAssessment'],
                                    'async': 'true'}
        results = post_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.NO_DATA)
        self.assertEqual(tasks[1][Constants.STATUS], Constants.NO_DATA)

    def test_generate_zip_file_name_for_grades(self):
        name = generate_zip_file_name('2016', ['6'], 'SUMMATIVE', ['MATH'])
        self.assertIn('ASMT_2016_GRADE_6_MATH_SUMMATIVE', name)

    def test_generate_zip_file_name_for_schools(self):
        name = generate_zip_file_name('2016', [None], 'SUMMATIVE', ['MATH', 'ELA'])
        self.assertIn('ASMT_2016_ELA_MATH_SUMMATIVE', name)

    def test_post_invalid_payload(self):
        self.assertRaises(EdApiHTTPPreconditionFailed, post_extract_service)

    def test_post_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, post_extract_service, self.__request)

    def test_get_invalid_param(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtSubject'] = ['MATH']
        self.__request.GET['asmyType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['districtGuid'] = '203'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_extract_service)

    def test_get_extract_service(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['districtGuid'] = '229'
        self.__request.GET['schoolGuid'] = '936'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtYear'] = '2016'
        response = get_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_post_extract_service(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NC'],
                                    'districtGuid': ['229'],
                                    'schoolGuid': ['936'],
                                    'asmtSubject': ['Math'],
                                    'asmtYear': ['2015'],
                                    'asmtType': ['SUMMATIVE']}
        response = post_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_post_extract_service_with_filters_and_selections(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NC'],
                                    'districtGuid': ['229'],
                                    'schoolGuid': ['939'],
                                    'asmtSubject': ['Math'],
                                    'asmtYear': ['2016'],
                                    'asmtType': ['SUMMATIVE'],
                                    'sex': ['male'],
                                    'asmtGrade': ['7'],
                                    'studentGuid': ['a629ca88-afe6-468c-9dbb-92322a284602']}
        response = post_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_get_valid_tenant_extract(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2015'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        results = get_extract_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.OK)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', results.json_body[ReportConstants.FILES][0][ReportConstants.DOWNLOAD_URL])

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_post_valid_tenant_extract(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': ['NC'],
                                    'asmtSubject': ['Math'],
                                    'asmtType': ['SUMMATIVE'],
                                    'asmtYear': ['2015'],
                                    'extractType': ['studentAssessment'],
                                    'async': 'true'}
        response = post_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/json')
        tasks = response.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.OK)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response.json_body[ReportConstants.FILES][0][ReportConstants.DOWNLOAD_URL])

    def test_with_no_sync_or_async_set(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2016'
        self.__request.GET['extractType'] = 'studentAssessment'
        response = get_extract_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_send_extraction_requesttest_get_extract_service(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['districtGuid'] = '229'
        self.__request.GET['schoolGuid'] = '936'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtYear'] = '2016'
        params = convert_query_string_to_dict_arrays(self.__request.GET)
        response = send_extraction_request(params)
        content_type = response._headerlist[0]
        self.assertEqual(content_type[1], "application/octet-stream")
        body = response.body
        tested = False
        with tempfile.TemporaryFile() as tmpfile:
            tmpfile.write(body)
            tmpfile.seek(0)
            myzipfile = zipfile.ZipFile(tmpfile)
            filelist = myzipfile.namelist()
            self.assertEqual(2, len(filelist))
            tested = True
        self.assertTrue(tested)

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_send_extraction_requesttest_get_extract_service_async(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtYear'] = '2015'
        self.__request.GET['extractType'] = 'studentAssessment'
        self.__request.GET['async'] = 'true'
        params = convert_query_string_to_dict_arrays(self.__request.GET)
        response = send_extraction_request(params)
        content_type = response._headerlist[0]
        self.assertEqual(content_type[1], "application/json; charset=UTF-8")
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response.json_body[ReportConstants.FILES][0][ReportConstants.DOWNLOAD_URL])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
