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
    get_pdf_content, _has_context_for_pdf_request, _get_school_name, _get_student_guids, _get_archive_name, \
    _get_merged_pdf_name, _create_student_guids
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

    def test_get_archive_name(self):
        name = _get_archive_name('School', 'en', False)
        start_in = 'student_reports_School_' in name
        end_in = '_en.zip' in name
        self.assertEqual(start_in, True)
        self.assertEquals(end_in, True)

    def test_get_archive_name_spanish(self):
        name = _get_archive_name('School', 'es', False)
        start_in = 'student_reports_School_' in name
        end_in = '_es.zip' in name
        self.assertEqual(start_in, True)
        self.assertEquals(end_in, True)

    def test_get_archive_name_grayscale(self):
        name = _get_archive_name('School', 'en', True)
        start_in = 'student_reports_School_' in name
        end_in = '_en.g.zip' in name
        self.assertEqual(start_in, True)
        self.assertEquals(end_in, True)

    def test_get_archive_name_space_in_name(self):
        name = _get_archive_name('School Name', 'en', False)
        start_in = 'student_reports_SchoolName_' in name
        end_in = '_en.zip' in name
        self.assertEqual(start_in, True)
        self.assertEquals(end_in, True)

    def test_get_archive_name_name_too_long(self):
        name = _get_archive_name('School Name Is Very Long Thing', 'en', False)
        start_in = 'student_reports_SchoolNameIsVer_' in name
        end_in = '_en.zip' in name
        self.assertEqual(start_in, True)
        self.assertEquals(end_in, True)

    def test_get_merged_pdf_name(self):
        name = _get_merged_pdf_name('School', '7', 'en', False)
        start_in = 'student_reports_School_grade_7_' in name
        end_in = '_en.pdf' in name
        self.assertEqual(start_in, True)
        self.assertEqual(end_in, True)

    def test_get_merged_pdf_name_grayscale(self):
        name = _get_merged_pdf_name('School', '7', 'en', True)
        start_in = 'student_reports_School_grade_7_' in name
        end_in = '_en.g.pdf' in name
        self.assertEqual(start_in, True)
        self.assertEqual(end_in, True)

    def test_get_merged_pdf_name_space_in_name(self):
        name = _get_merged_pdf_name('School Name', '7', 'en', False)
        start_in = 'student_reports_SchoolName_grade_7_' in name
        end_in = '_en.pdf' in name
        self.assertEqual(start_in, True)
        self.assertEqual(end_in, True)

    def test_get_merged_pdf_name_name_too_long(self):
        name = _get_merged_pdf_name('School Name Is Very Long Thing', '7', 'en', False)
        start_in = 'student_reports_SchoolNameIsVer_grade_7_' in name
        end_in = '_en.pdf' in name
        self.assertEqual(start_in, True)
        self.assertEqual(end_in, True)

    def test_get_merged_pdf_name_all_grade(self):
        name = _get_merged_pdf_name('School', 'all', 'en', False)
        start_in = 'student_reports_School_' in name
        grade_not_in = '_grade_' not in name
        end_in = '_en.pdf' in name
        self.assertEqual(start_in, True)
        self.assertEqual(grade_not_in, True)
        self.assertEqual(end_in, True)

    def test_create_student_guids_by_guids(self):
        all_guids, guids_by_grade = _create_student_guids(['1', '2', '3'], None, 'NC', None, None, 'SUMMATIVE',
                                                          '20160404', {})
        self.assertEqual(len(all_guids), 3)
        self.assertIn('all', guids_by_grade)
        self.assertEqual(len(guids_by_grade['all']), 3)

    def test_create_student_guids_by_grade(self):
        all_guids, guids_by_grade = _create_student_guids(None, ['7', '8'], 'NC', '229', '939', 'SUMMATIVE',
                                                          '20160404', {})
        self.assertEqual(len(all_guids), 10)
        self.assertIn('7', guids_by_grade)
        self.assertIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['7']), 8)
        self.assertEqual(len(guids_by_grade['8']), 2)

    def test_create_student_guids_by_grade_group(self):
        all_guids, guids_by_grade = _create_student_guids(None, ['7', '8'], 'NC', '229', '939', 'SUMMATIVE',
                                                          '20160404', {'group1Id': ['d20236e0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(all_guids), 5)
        self.assertIn('7', guids_by_grade)
        self.assertNotIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['7']), 5)

    def test_create_student_guids_by_guids_no_students(self):
        self.assertRaises(InvalidParameterError, _create_student_guids, [], None, 'NC', '229', '939', 'SUMMATIVE',
                          '20160404', {})

    def test_create_student_guids_by_grade_no_students(self):
        self.assertRaises(InvalidParameterError, _create_student_guids, None, ['7'], 'NC', '229', '939', 'SUMMATIVE',
                          '20160404', {'sex': ['not_stated']})

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
