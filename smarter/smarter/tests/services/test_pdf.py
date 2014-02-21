'''
Created on May 17, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from edapi.httpexceptions import EdApiHTTPPreconditionFailed, \
    EdApiHTTPForbiddenAccess, EdApiHTTPNotFound, EdApiHTTPInternalServerError
from edapi.tests.test_views import DummyValueError
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
import services
from pyramid.response import Response
from smarter.services.pdf import post_pdf_service, get_pdf_service, send_pdf_request, \
    get_pdf_content, has_context_for_pdf_request
from edapi.exceptions import InvalidParameterError, ForbiddenError
from services.celery import setup_celery
import tempfile
from pyramid.registry import Registry
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from services.tasks.pdf import prepare_path
#from services.celeryconfig import get_config
import shutil
from edauth.security.session import Session
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.student import Student  # @UnusedImport
from services.tests.tasks.test_pdf import get_cmd


class TestServices(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        self.__temp_dir = tempfile.mkdtemp()
        reg.settings = {}
        reg.settings['pdf.report_base_dir'] = self.__temp_dir
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
            connection.execute(user_mapping.insert(), user_id='1020', guid='1020')
            connection.execute(user_mapping.insert(), user_id='a5ddfe12-740d-4487-9179-de70f6ac33be', guid='a5ddfe12-740d-4487-9179-de70f6ac33be')
        dummy_session = Session()
        dummy_session.set_roles(['STUDENT'])
        dummy_session.set_uid('a5ddfe12-740d-4487-9179-de70f6ac33be')
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)
        # celery settings for UT
        settings = {'services.celery.CELERY_ALWAYS_EAGER': True}
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        setup_celery(settings)

    def tearDown(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)
        self.__request = None
        testing.tearDown()
        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_post_pdf_serivce_post_invalid_payload(self):
        self.assertRaises(EdApiHTTPPreconditionFailed, post_pdf_service, DummyValueError())

    def test_post_pdf_service_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, post_pdf_service, self.__request)

    def test_post_pdf_service_no_context(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'studentGuid': 'a016a4c1-5aca-4146-a85b-ed1172a01a4d', 'stateCode': 'NC'}
        dummy_session = Session()
        dummy_session.set_roles(['STUDENT'])
        dummy_session.set_uid('1020')
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)

        self.assertRaises(EdApiHTTPForbiddenAccess, post_pdf_service, None, self.__request)

    def test_post_pdf_service_post_valid_payload(self):
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        self.__request.method = 'POST'
        self.__request.json_body = {'studentGuid': studentGuid, 'stateCode': 'NC'}
        self.__request.cookies = {'edware': '123'}
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', pdf_report_base_dir=self.__temp_dir, student_guid=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file)
        with open(pdf_file, 'w') as file:
            file.write('%PDF-1.4')
        response = post_pdf_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_get_pdf_service_invalid_param(self):
        self.__request.GET = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, get_pdf_service, self.__request)

    def test_get_pdf_service_invalid_report_name(self):
        self.__request.GET = {}
        self.__request.matchdict['report'] = 'newReport'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_pdf_service, self.__request)

    def test_get_pdf_service_no_context(self):
        self.__request.method
        self.__request.GET = {'studentGuid': 'a016a4c1-5aca-4146-a85b-ed1172a01a4d', 'stateCode': 'NC'}
        dummy_session = Session()
        dummy_session.set_roles(['STUDENT'])
        dummy_session.set_uid('1020')
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)
        self.__request.matchdict['report'] = 'indivStudentReport.html'

        self.assertRaises(EdApiHTTPForbiddenAccess, get_pdf_service, None, self.__request)

    def test_get_pdf_valid_params(self):
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        self.__request.GET['studentGuid'] = studentGuid
        self.__request.GET['stateCode'] = 'NC'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', pdf_report_base_dir=self.__temp_dir, student_guid=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file)
        with open(pdf_file, 'w') as file:
            file.write('%PDF-1.4')
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        response = get_pdf_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_send_pdf_request(self):
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params = {}
        params['studentGuid'] = studentGuid
        params['stateCode'] = 'NC'
        params['dummy'] = 'dummy'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', pdf_report_base_dir=self.__temp_dir, student_guid=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file)
        with open(pdf_file, 'w') as file:
            file.write('%PDF-1.4')
        response = send_pdf_request(params)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/pdf')
        self.assertIsInstance(response.body, bytes)

    def test_send_pdf_request_with_pdf_generation_fail(self):
        dummy_session = Session()
        dummy_session.set_roles(['TEACHER'])
        dummy_session.set_uid('1020')
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)
        params = {}
        # Important, this pdf must not exist in directory
        params['studentGuid'] = '3181376a-f3a8-40d3-bbde-e65fdd9f4494'
        params['stateCode'] = 'NC'
        params['dummy'] = 'dummy'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = get_cmd()
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params)

    def test_get_pdf_content_with_missing_student_guid(self):
        params = {}
        self.assertRaises(InvalidParameterError, get_pdf_content, params)

    def test_get_pdf_content_with_no_context(self):
        params = {}
        params['studentGuid'] = 'a016a4c1-5aca-4146-a85b-ed1172a01a4d'
        params['stateCode'] = 'NC'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        dummy_session = Session()
        dummy_session.set_roles(['STUDENT'])
        dummy_session.set_uid('1020')
        dummy_session.set_tenants([self.__tenant_name])
        self.__config.testing_securitypolicy(dummy_session)

        self.assertRaises(ForbiddenError, get_pdf_content, params)

    def test_has_context_for_pdf_request(self):
        student_guid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        has_context = has_context_for_pdf_request('NC', student_guid)
        self.assertTrue(has_context)

    def test_has_context_for_pdf_request_with_no_context(self):
        student_guid = 'invalid'
        has_context = has_context_for_pdf_request('NC', student_guid)
        self.assertFalse(has_context)

    def test_send_pdf_request_with_always_generate_flag(self):
        self.__config.registry.settings['pdf.always_generate'] = 'True'
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params = {}
        params['studentGuid'] = studentGuid
        params['stateCode'] = 'NC'
        params['dummy'] = 'dummy'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = get_cmd()
        # prepare empty file to mimic a pdf was generated
        pdf_file = generate_isr_report_path_by_student_guid('NC', pdf_report_base_dir=self.__temp_dir, student_guid=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file)
        with open(pdf_file, 'w') as file:
            file.write('%PDF-1.4')
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
