__author__ = 'sravi'

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
from smarter.services.raw_extract import post_raw_data_service, get_raw_data_service, generate_zip_file_name, \
    send_extraction_request
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
import smarter.extracts.format
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from edcore.security.tenant import set_tenant_map
from smarter_common.security.constants import RolesConstants
from smarter.security.roles.pii import PII  # @UnusedImport


class TestRawExtract(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

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

    def test_post_valid_response_raw_extract(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': 'NC',
                                    'asmtYear': '2018',
                                    'asmtType': 'SUMMATIVE',
                                    'asmtSubject': 'Math',
                                    'asmtGrade': '3',
                                    'extractType': 'rawData',
                                    'async': 'true'}
        results = post_raw_data_service(None, self.__request)
        self.assertIsInstance(results, Response)
        self.assertEqual(len(results.json_body['tasks']), 1)
        self.assertEqual(results.json_body['tasks'][0][Constants.STATUS], Constants.FAIL)

    def test_get_valid_response_raw_extract(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '2016'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        response = get_raw_data_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_get_missing_param_raw_extract(self):
        """Missing asmtYear"""
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        self.__request.GET['async'] = 'true'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_raw_data_service)

    def test_get_invalid_param_raw_extract(self):
        """asmtYear has letters"""
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '201a'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        self.__request.GET['async'] = 'true'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_raw_data_service)

    def test_generate_zip_file_name(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2016',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '6'}
        name = generate_zip_file_name(params)
        self.assertIn('RAW_NC_2016_SUMMATIVE_MATH_GRADE_6', name)

    def test_post_invalid_payload(self):
        self.assertRaises(EdApiHTTPPreconditionFailed, post_raw_data_service)

    def test_post_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, post_raw_data_service, self.__request)

    def test_get_invalid_param(self):
        """Letter in asmtGrade"""
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '2016'
        self.__request.GET['asmyType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3b'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_raw_data_service)

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_get_valid_raw_extract(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '2015'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        self.__request.GET['async'] = 'true'
        results = get_raw_data_service(None, self.__request)
        self.assertIsInstance(results, Response)
        tasks = results.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.OK)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', results.json_body['download_url'])

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_post_valid_raw_extract(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        self.__request.method = 'POST'
        self.__request.json_body = {'stateCode': 'NC',
                                    'asmtYear': '2015',
                                    'asmtType': 'SUMMATIVE',
                                    'asmtSubject': 'Math',
                                    'asmtGrade': '3',
                                    'extractType': 'rawData',
                                    'async': 'true'}
        response = post_raw_data_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/json')
        tasks = response.json_body['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][Constants.STATUS], Constants.OK)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response.json_body['download_url'])

    def test_with_no_sync_or_async_set(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '2016'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        response = get_raw_data_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/octet-stream')

    def test_send_extraction_request_sync(self):
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '2016'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        response = send_extraction_request(self.__request.GET)
        content_type = response._headerlist[0]
        self.assertEqual(content_type[1], "application/octet-stream")
        body = response.body
        tested = False
        with tempfile.TemporaryFile() as tmpfile:
            tmpfile.write(body)
            tmpfile.seek(0)
            myzipfile = zipfile.ZipFile(tmpfile)
            filelist = myzipfile.namelist()
            self.assertEqual(21, len(filelist))
            tested = True
        self.assertTrue(tested)

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_send_extraction_request_async(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['asmtYear'] = '2015'
        self.__request.GET['asmtType'] = 'SUMMATIVE'
        self.__request.GET['asmtSubject'] = 'Math'
        self.__request.GET['asmtGrade'] = '3'
        self.__request.GET['extractType'] = 'rawData'
        self.__request.GET['async'] = 'true'
        response = send_extraction_request(self.__request.GET)
        content_type = response._headerlist[0]
        self.assertEqual(content_type[1], "application/json; charset=UTF-8")
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response.json_body['download_url'])


if __name__ == "__main__":
    unittest.main()
