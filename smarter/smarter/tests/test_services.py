'''
Created on May 17, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from edapi.httpexceptions import EdApiHTTPPreconditionFailed, \
    EdApiHTTPForbiddenAccess
from edapi.tests.test_views import DummyValueError
from smarter.database.connector import SmarterDBConnection
from edauth.security.user import User
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
import services
from pyramid.response import Response
from smarter.services import post_pdf_service, get_pdf_service, send_pdf_request, \
    get_pdf_content, has_context_for_pdf_request
from edapi.exceptions import InvalidParameterError, ForbiddenError
from services.celery import setup_celery
import tempfile
from pyramid.registry import Registry
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from services.tasks.create_pdf import prepare_file_path


class TestServices(Unittest_with_smarter_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        self.__temp_dir = tempfile.gettempdir()
        reg['pdf.report_base_dir'] = self.__temp_dir
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        with SmarterDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
            connection.execute(user_mapping.insert(), user_id='1020', guid='1020')
        dummy_user = User()
        dummy_user.set_roles(['TEACHER'])
        dummy_user.set_uid('272')
        self.__config.testing_securitypolicy(dummy_user)
        # celery settings for UT
        settings = {'celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)

    def tearDown(self):
        self.__request = None
        testing.tearDown()
        # delete user_mapping entries
        with SmarterDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_post_pdf_serivce_post_invalid_payload(self):
        self.assertRaises(EdApiHTTPPreconditionFailed, post_pdf_service, DummyValueError())

    def test_post_pdf_service_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, post_pdf_service, self.__request)

    def test_post_pdf_service_no_context(self):
        self.__request.json_body = {'studentGuid': 'a016a4c1-5aca-4146-a85b-ed1172a01a4d'}
        dummy_user = User()
        dummy_user.set_roles(['TEACHER'])
        dummy_user.set_uid('1020')
        self.__config.testing_securitypolicy(dummy_user)

        self.assertRaises(EdApiHTTPForbiddenAccess, post_pdf_service, self.__request)

    def test_post_pdf_service_post_valid_payload(self):
        self.__request.json_body = {'studentGuid': 'a5ddfe12-740d-4487-9179-de70f6ac33be'}
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # Override the wkhtmltopdf command
        services.tasks.create_pdf.pdf_procs = ['echo', 'dummy']
        response = post_pdf_service(self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_get_pdf_service_invalid_param(self):
        self.__request.GET = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, get_pdf_service, self.__request)

    def test_get_pdf_service_no_context(self):
        self.__request.GET = {'studentGuid': 'a016a4c1-5aca-4146-a85b-ed1172a01a4d'}
        dummy_user = User()
        dummy_user.set_roles(['TEACHER'])
        dummy_user.set_uid('1020')
        self.__config.testing_securitypolicy(dummy_user)

        self.assertRaises(EdApiHTTPForbiddenAccess, get_pdf_service, self.__request)

    def test_get_pdf_valid_params(self):
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        self.__request.GET['studentGuid'] = studentGuid
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid(pdf_report_base_dir=self.__temp_dir, student_guid=studentGuid, asmt_type='SUMMATIVE')
        prepare_file_path(pdf_file)
        with open(pdf_file, 'w') as file:
            file.write('%PDF-1.4')
        # Override the wkhtmltopdf command
        services.tasks.create_pdf.pdf_procs = ['echo', 'dummy']
        response = get_pdf_service(self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_send_pdf_request(self):
        params = {}
        params['studentGuid'] = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params['dummy'] = 'dummy'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.create_pdf.pdf_procs = ['echo', 'dummy']
        response = send_pdf_request(params)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/pdf')
        self.assertIsInstance(response.body, bytes)

    def test_get_pdf_content_with_missing_student_guid(self):
        params = {}
        self.assertRaises(InvalidParameterError, get_pdf_content, params)

    def test_get_pdf_content_with_no_context(self):
        params = {}
        params['studentGuid'] = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        dummy_user = User()
        dummy_user.set_roles(['TEACHER'])
        dummy_user.set_uid('1020')
        self.__config.testing_securitypolicy(dummy_user)

        self.assertRaises(ForbiddenError, get_pdf_content, params)

    def test_has_context_for_pdf_request(self):
        student_guid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        has_context = has_context_for_pdf_request(student_guid)
        self.assertTrue(has_context)

    def test_has_context_for_pdf_request_with_no_context(self):
        student_guid = 'invalid'
        has_context = has_context_for_pdf_request(student_guid)
        self.assertFalse(has_context)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
