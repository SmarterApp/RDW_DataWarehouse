'''
Created on May 17, 2013

@author: dip
'''
import unittest
import tempfile
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.response import Response
from pyramid.registry import Registry
from edapi.httpexceptions import EdApiHTTPPreconditionFailed, \
    EdApiHTTPForbiddenAccess, EdApiHTTPInternalServerError, EdApiHTTPNotFound
from edapi.tests.test_views import DummyValueError
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    get_unittest_tenant_name
import services
from smarter.services.pdf import post_pdf_service, get_pdf_service, send_pdf_request, \
    get_pdf_content, _has_context_for_pdf_request, _get_school_name, _get_student_guids
from edapi.exceptions import InvalidParameterError, ForbiddenError
from services.celery import setup_celery
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from services.tasks.pdf import prepare_path
import shutil
from services.tests.tasks.test_pdf import get_cmd
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport
from pyramid.security import Allow
import edauth
from edcore.security.tenant import set_tenant_map
from smarter_common.security.constants import RolesConstants
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from smarter.reports.helpers.constants import Constants
from unittest.mock import patch


class TestServices(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        # Set up defined roles
        self.__tenant_name = get_unittest_tenant_name()
        set_tenant_map({self.__tenant_name: "NC"})
        self.__temp_dir = tempfile.mkdtemp()
        reg.settings = {}
        reg.settings['pdf.report_base_dir'] = self.__temp_dir
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, self.__tenant_name, 'NC', '228', '242'),
                                        RoleRelation(RolesConstants.PII, self.__tenant_name, 'NC', '229', '939')])
        self.__config.testing_securitypolicy(dummy_session.get_user())

        # celery settings for UT
        settings = {'services.celery.CELERY_ALWAYS_EAGER': True}
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        setup_celery(settings)

    def tearDown(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)
        self.__request = None
        testing.tearDown()

    def test_post_pdf_serivce_post_invalid_payload(self):
        self.assertRaises(EdApiHTTPPreconditionFailed, post_pdf_service, DummyValueError())

    def test_post_pdf_service_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, post_pdf_service, self.__request)

    def test_post_pdf_service_no_context(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'studentGuid': ['19489898-d469-41e2-babc-265ecbab2337'], 'stateCode': 'NC', 'effectiveDate': 20160404}

        self.assertRaises(EdApiHTTPForbiddenAccess, post_pdf_service, None, self.__request)

    def test_post_pdf_service_post_valid_payload(self):
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        self.__request.method = 'POST'
        self.__request.json_body = {'studentGuid': [studentGuid], 'stateCode': 'NC', 'effectiveDate': 20160404}
        self.__request.cookies = {'edware': '123'}
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
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
        self.__request.GET = {'studentGuid': '19489898-d469-41e2-babc-265ecbab2337', 'stateCode': 'NC', 'effectiveDate': 20160404}
        self.__request.matchdict['report'] = 'indivStudentReport.html'

        self.assertRaises(EdApiHTTPForbiddenAccess, get_pdf_service, None, self.__request)

    def test_get_pdf_valid_params(self):
        studentGuid = 'a016a4c1-5aca-4146-a85b-ed1172a01a4d'
        self.__request.GET['studentGuid'] = studentGuid
        self.__request.GET['stateCode'] = 'NC'
        self.__request.GET['effectiveDate'] = 20160404
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
            file.write('%PDF-1.4')
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        response = get_pdf_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_send_pdf_request(self):
        studentGuid = "a016a4c1-5aca-4146-a85b-ed1172a01a4d"
        params = {}
        params['studentGuid'] = studentGuid
        params['stateCode'] = 'NC'
        params['effectiveDate'] = 20160404
        params['dummy'] = 'dummy'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
            file.write('%PDF-1.4')
        response = send_pdf_request(params)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, 'application/pdf')
        self.assertIsInstance(response.body, bytes)

    def test_send_pdf_request_with_pdf_generation_fail(self):
        params = {}
        # Important, this pdf must not exist in directory
        params['studentGuid'] = '3181376a-f3a8-40d3-bbde-e65fdd9f4494'
        params['stateCode'] = 'NC'
        params['effectiveDate'] = 20160404
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
        params['studentGuid'] = '19489898-d469-41e2-babc-265ecbab2337'
        params['stateCode'] = 'NC'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        self.assertRaises(ForbiddenError, get_pdf_content, params)

    def test_has_context_for_pdf_request(self):
        student_guid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        has_context = _has_context_for_pdf_request('NC', student_guid)
        self.assertTrue(has_context)

    def test_has_context_for_pdf_request_with_no_context(self):
        student_guid = 'invalid'
        has_context = _has_context_for_pdf_request('NC', student_guid)
        self.assertFalse(has_context)

    def test_send_pdf_request_with_always_generate_flag(self):
        self.__config.registry.settings['pdf.always_generate'] = 'True'
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params = {}
        params['studentGuid'] = studentGuid
        params['stateCode'] = 'NC'
        params['dummy'] = 'dummy'
        params['effectiveDate'] = 20160404
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = get_cmd()
        # prepare empty file to mimic a pdf was generated
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type='SUMMATIVE')
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
            file.write('%PDF-1.4')
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params)

    def test_send_pdf_request_no_such_report(self):
        self.__request.matchdict['report'] = 'fake_report.html'
        self.assertRaises(EdApiHTTPNotFound, send_pdf_request, {})

    def test_send_pdf_request_fail_precondition(self):
        params = {}
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.assertRaises(EdApiHTTPPreconditionFailed, send_pdf_request, params)

    def test_get_pdf_content_InvalidParameterError(self):
        params = {}
        params['studentGuid'] = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params['stateCode'] = 'NC'
        params[Constants.ASMTTYPE] = 'FAKE'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        self.assertRaises(InvalidParameterError, get_pdf_content, params)

    @patch('smarter.services.pdf._start_bulk')
    @patch('smarter.services.pdf.generate_isr_report_path_by_student_guid')
    @patch('smarter.services.pdf.register_file')
    def test_get_pdf_content(self, mock_register_file, mock_generate_isr_report_path_by_student_guid_patch, mock_start_bulk):
        mock_register_file.return_value = (1, 'http://foo.com/foo')
        mock_generate_isr_report_path_by_student_guid_patch.return_value = {'a5ddfe12-740d-4487-9179-de70f6ac33be': '/a', '34140997-8949-497e-bbbb-5d72aa7dc9cb': '/b'}
        params = {}
        params['studentGuid'] = ['a5ddfe12-740d-4487-9179-de70f6ac33be', '34140997-8949-497e-bbbb-5d72aa7dc9cb']
        params['stateCode'] = 'NC'
        self.__request.matchdict['report'] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        response = get_pdf_content(params)
        pass

    def test_get_school_name(self):
        name = _get_school_name('NC', '229', '939')
        self.assertEqual(name, 'Daybreak - Western Middle')

    def test_get_school_name_invalid(self):
        self.assertRaises(InvalidParameterError, _get_school_name, 'NC', 'Bad', 'Bad')

    def test_get_student_guids(self):
        guids = _get_student_guids('NC', '229', '939', '7', 'SUMMATIVE', '20160404', {})
        self.assertEqual(len(guids), 8)

    def test_get_student_guids_males(self):
        guids = _get_student_guids('NC', '229', '939', '7', 'SUMMATIVE', '20160404', {'sex': ['male']})
        self.assertEqual(len(guids), 4)

    def test_get_student_guids_group1(self):
        guids = _get_student_guids('NC', '229', '939', '7', 'SUMMATIVE', '20160404', {'group1Id': ['d20236e0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(guids), 5)

    def test_get_student_guids_group2(self):
        guids = _get_student_guids('NC', '229', '939', '7', 'SUMMATIVE', '20160404', {'group2Id': ['ee7bcbb0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(guids), 6)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
