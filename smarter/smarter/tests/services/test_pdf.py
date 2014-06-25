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
from edapi.exceptions import NotFoundException as APINotFoundException
from edapi.exceptions import ForbiddenError as APIForbiddenError
from edapi.tests.test_views import DummyValueError
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, \
    get_unittest_tenant_name
import services
from smarter.services.pdf import post_pdf_service, get_pdf_service, send_pdf_request, \
    get_pdf_content, _has_context_for_pdf_request, _get_school_name, _get_student_guids, _get_archive_name, \
    _get_merged_pdf_name, _create_student_guids, get_single_pdf_content, \
    _create_student_pdf_url, _create_pdf_merge_tasks, \
    _create_urls_by_student_guid, get_bulk_pdf_content,\
    _create_pdf_generate_tasks
from edapi.exceptions import InvalidParameterError, ForbiddenError
from services.celery import setup_celery
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from services.tasks.pdf import prepare_path
import shutil
from services.tests.tasks.test_pdf import get_cmd
from pyramid.security import Allow
import edauth
from edcore.security.tenant import set_tenant_map
from smarter_common.security.constants import RolesConstants
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from smarter.reports.helpers.constants import Constants, AssessmentType
from unittest.mock import patch
import json
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport


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
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
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
        self.__request.json_body = {Constants.STUDENTGUID: ['19489898-d469-41e2-babc-265ecbab2337'], Constants.STATECODE: 'NC', Constants.ASMTTYPE: AssessmentType.SUMMATIVE, Constants.EFFECTIVEDATE: 20160404}

        self.assertRaises(EdApiHTTPForbiddenAccess, post_pdf_service, None, self.__request)

    # def test_post_pdf_service_post_valid_payload(self):
    #     studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
    #     self.__request.method = 'POST'
    #     self.__request.json_body = {Constants.STUDENTGUID: [studentGuid], Constants.STATECODE: 'NC',
    #                                 Constants.ASMTTYPE: AssessmentType.SUMMATIVE, Constants.EFFECTIVEDATE: 20160404,
    #                                 Constants.DISTRICTGUID: '229', Constants.SCHOOLGUID: '939'}
    #     self.__request.cookies = {'edware': '123'}
    #     # Override the wkhtmltopdf command
    #     services.tasks.pdf.pdf_procs = ['echo', 'dummy']
    #     # prepare empty file
    #     pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir,
    #                                                         student_guids=studentGuid,
    #                                                         asmt_type=AssessmentType.SUMMATIVE)
    #     prepare_path(pdf_file[studentGuid])
    #     with open(pdf_file[studentGuid], 'w') as file:
    #         file.write('%PDF-1.4')
    #     response = post_pdf_service(None, self.__request)
    #     self.assertIsInstance(response, Response)
    #     self.assertIsNotNone(response.body)
    #     self.assertEqual(response.content_type, Constants.APPLICATION_PDF)

    def test_get_pdf_service_invalid_param(self):
        self.__request.GET = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, get_pdf_service, self.__request)

    def test_get_pdf_service_invalid_report_name(self):
        self.__request.GET = {}
        self.__request.matchdict[Constants.REPORT] = 'newReport'
        self.assertRaises(EdApiHTTPPreconditionFailed, get_pdf_service, self.__request)

    def test_get_pdf_service_no_context(self):
        self.__request.method
        self.__request.GET = {Constants.STUDENTGUID: '19489898-d469-41e2-babc-265ecbab2337', Constants.STATECODE: 'NC', Constants.EFFECTIVEDATE: 20160404}
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'

        self.assertRaises(EdApiHTTPForbiddenAccess, get_pdf_service, None, self.__request)

    def test_get_pdf_valid_params(self):
        studentGuid = 'a016a4c1-5aca-4146-a85b-ed1172a01a4d'
        self.__request.GET[Constants.STUDENTGUID] = studentGuid
        self.__request.GET[Constants.STATECODE] = 'NC'
        self.__request.GET[Constants.EFFECTIVEDATE] = 20160404
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
            file.write('%PDF-1.4')
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        response = get_pdf_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, Constants.APPLICATION_PDF)

    def test_send_pdf_request(self):
        studentGuid = "a016a4c1-5aca-4146-a85b-ed1172a01a4d"
        params = {}
        params[Constants.STUDENTGUID] = studentGuid
        params[Constants.STATECODE] = 'NC'
        params[Constants.EFFECTIVEDATE] = 20160404
        params['dummy'] = 'dummy'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
            file.write('%PDF-1.4')
        response = send_pdf_request(params)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.content_type, Constants.APPLICATION_PDF)
        self.assertIsInstance(response.body, bytes)

    def test_send_pdf_request_with_pdf_generation_fail(self):
        params = {}
        # Important, this pdf must not exist in directory
        params[Constants.STUDENTGUID] = '3181376a-f3a8-40d3-bbde-e65fdd9f4494'
        params[Constants.STATECODE] = 'NC'
        params[Constants.EFFECTIVEDATE] = 20160404
        params['dummy'] = 'dummy'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = get_cmd()
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params)

    def test_get_pdf_content_with_missing_student_guid(self):
        params = {}
        self.assertRaises(InvalidParameterError, get_pdf_content, params)

    def test_get_pdf_content_with_no_context(self):
        params = {}
        params[Constants.STUDENTGUID] = '19489898-d469-41e2-babc-265ecbab2337'
        params[Constants.STATECODE] = 'NC'
        params[Constants.ASMTTYPE] = 'SUMMATIVE'
        params[Constants.ASMTYEAR] = '2016'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
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
        params[Constants.STUDENTGUID] = studentGuid
        params[Constants.STATECODE] = 'NC'
        params['dummy'] = 'dummy'
        params[Constants.EFFECTIVEDATE] = 20160404
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = get_cmd()
        # prepare empty file to mimic a pdf was generated
        pdf_file = generate_isr_report_path_by_student_guid('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_guids=studentGuid, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentGuid])
        with open(pdf_file[studentGuid], 'w') as file:
            file.write('%PDF-1.4')
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params)

    def test_send_pdf_request_no_such_report(self):
        self.__request.matchdict[Constants.REPORT] = 'fake_report.html'
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, {})

    def test_send_pdf_request_fail_precondition(self):
        params = {}
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.assertRaises(EdApiHTTPPreconditionFailed, send_pdf_request, params)

    def test_get_pdf_content_InvalidParameterError(self):
        params = {}
        params[Constants.STUDENTGUID] = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params[Constants.STATECODE] = 'NC'
        params[Constants.ASMTTYPE] = 'FAKE'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        self.assertRaises(InvalidParameterError, get_pdf_content, params)

    def test_get_school_name(self):
        name = _get_school_name('NC', '229', '939')
        self.assertEqual(name, 'Daybreak - Western Middle')

    def test_get_school_name_invalid(self):
        self.assertRaises(InvalidParameterError, _get_school_name, 'NC', 'Bad', 'Bad')

    def test_get_student_guids(self):
        guids = _get_student_guids('NC', '229', '939', '7', AssessmentType.SUMMATIVE, '2016', '20160404', {})
        self.assertEqual(len(guids), 8)

    def test_get_student_guids_males(self):
        guids = _get_student_guids('NC', '229', '939', '7', AssessmentType.SUMMATIVE, '2016', '20160404', {'sex': ['male']})
        self.assertEqual(len(guids), 4)

    def test_get_student_guids_group1(self):
        guids = _get_student_guids('NC', '229', '939', '7', AssessmentType.SUMMATIVE, '2016', '20160404', {'group1Id': ['d20236e0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(guids), 5)

    def test_get_student_guids_group2(self):
        guids = _get_student_guids('NC', '229', '939', '7', AssessmentType.SUMMATIVE, '2016', '20160404', {'group2Id': ['ee7bcbb0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(guids), 6)

    def test_get_student_guids_alphabetical(self):
        recs = _get_student_guids('NC', '229', '939', '7', AssessmentType.SUMMATIVE, '2016', '20160404', {})
        name = None
        for record in recs:
            if name is not None:
                self.assertLess(name, record['last_name'] + ', ' + record['first_name'])
            name = record['last_name'] + ', ' + record['first_name']

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
        all_guids, guids_by_grade = _create_student_guids(['1', '2', '3'], None, 'NC', None, None, AssessmentType.SUMMATIVE,
                                                          '2016', '20160404', {})
        self.assertEqual(len(all_guids), 3)
        self.assertIn('all', guids_by_grade)
        self.assertEqual(len(guids_by_grade['all']), 3)

    def test_create_student_guids_by_grade(self):
        all_guids, guids_by_grade = _create_student_guids(None, ['7', '8'], 'NC', '229', '939', AssessmentType.SUMMATIVE,
                                                          '2016', '20160404', {})
        self.assertEqual(len(all_guids), 10)
        self.assertIn('7', guids_by_grade)
        self.assertIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['7']), 8)
        self.assertEqual(len(guids_by_grade['8']), 2)

    def test_create_student_guids_by_grade_group(self):
        all_guids, guids_by_grade = _create_student_guids(None, ['7', '8'], 'NC', '229', '939', AssessmentType.SUMMATIVE,
                                                          '2016', '20160404',
                                                          {'group1Id': ['d20236e0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(all_guids), 5)
        self.assertIn('7', guids_by_grade)
        self.assertNotIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['7']), 5)

    def test_create_student_guids_by_guids_no_students(self):
        self.assertRaises(InvalidParameterError, _create_student_guids, [], None, 'NC', '229', '939', AssessmentType.SUMMATIVE,
                          '2016', '20160404', {})

    def test_create_student_guids_by_grade_no_students(self):
        self.assertRaises(InvalidParameterError, _create_student_guids, None, ['7'], 'NC', '229', '939', AssessmentType.SUMMATIVE,
                          '2016', '20160404', {'sex': ['not_stated']})

    @patch('smarter.services.pdf.get.delay')
    def test_get_single_pdf_content(self, mock_get):
        mock_get.return_value.get.return_value = 'BIG PDF CONTENT STUFF'.encode()
        response = get_single_pdf_content('/tmp', 'localhost/', '123', 'edware', 30, 'NC', '2016', '20160404', AssessmentType.SUMMATIVE,
                                          'a629ca88-afe6-468c-9dbb-92322a284602', 'en', False, False, 30, {})
        self.assertEqual(response.status_code, 200)

    @patch('smarter.services.pdf.get')
    def test_get_single_pdf_content_bad_effective_date(self, mock_get):
        mock_get.return_value = None
        self.assertRaises(APINotFoundException, get_single_pdf_content, '/tmp', 'localhost/', '123', 'edware', 30, 'NC',
                          '2016', '20160304', AssessmentType.SUMMATIVE, 'a629ca88-afe6-468c-9dbb-92322a284602', 'en',
                          False, False, 30, {})

    @patch('smarter.services.pdf.get')
    def test_get_single_pdf_content_bad_student_guid(self, mock_get):
        mock_get.return_value = None
        self.assertRaises(APIForbiddenError, get_single_pdf_content, '/tmp', 'localhost/', '123', 'edware', 30, 'NC',
                          '2016', '20160404', AssessmentType.SUMMATIVE, 'a629ca88-afe6-468c-9dbb', 'en', False, False,
                          30, {})

    def test_create_student_pdf_url(self):
        student_guid = '1-2-3-4-5'
        base_url = 'http://foo.com/foo'
        params = {}
        result = _create_student_pdf_url(student_guid, base_url, params)
        self.assertIn(result, ['http://foo.com/foo?pdf=true&studentGuid=1-2-3-4-5', 'http://foo.com/foo?studentGuid=1-2-3-4-5&pdf=true'])
        params = {'abc': 'ef'}
        result = _create_student_pdf_url(student_guid, base_url, params)
        self.assertTrue('abc=ef' in result)

    def test_create_pdf_merge_tasks_no_guid(self):
        pdf_base_dir = '/base'
        directory_to_archive = '/foo'
        guids_by_grade = []
        files_by_guid = {'a5ddfe12-740d-4487-9179-de70f6ac33be': '/foo/abc.pdf'}
        school_name = 'schoolname here'
        lang = 'en'
        is_grayscale = None
        tasks = _create_pdf_merge_tasks(pdf_base_dir, directory_to_archive, guids_by_grade, files_by_guid, school_name, lang, is_grayscale)
        self.assertEqual(0, len(tasks))
        guids_by_grade = {'3': 'a5ddfe12-740d-4487-9179-de70f6ac33be'}
        tasks = _create_pdf_merge_tasks(pdf_base_dir, directory_to_archive, guids_by_grade, files_by_guid, school_name, lang, is_grayscale)
        self.assertEqual(1, len(tasks))

    def test_create_pdf_merge_tasks_with_guids(self):
        pdf_base_dir = '/foo'
        directory_to_archive = '/archive'
        guids_by_grade = {'2': ['1-2-3-4', 'a-b-c-d'], '3': '4-3-2-1'}
        files_by_guid = {'1-2-3-4': '/foo/1.pdf', 'a-b-c-d': '/foo/2.pdf', '4-3-2-1': '/foo/3.pdf'}
        school_name = 'Apple School'
        lang = 'en'
        is_grayscale = False
        tasks = _create_pdf_merge_tasks(pdf_base_dir, directory_to_archive, guids_by_grade, files_by_guid, school_name, lang, is_grayscale)
        self.assertEqual(2, len(tasks))

    def test_create_urls_by_student_guid(self):
        studentGuid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        baseURL = 'http://foo.com/abc'
        url = _create_urls_by_student_guid(studentGuid, 'NC', baseURL, {})
        self.assertIn(url['a5ddfe12-740d-4487-9179-de70f6ac33be'], ['http://foo.com/abc?pdf=true&studentGuid=a5ddfe12-740d-4487-9179-de70f6ac33be',
                                                                    'http://foo.com/abc?studentGuid=a5ddfe12-740d-4487-9179-de70f6ac33be&pdf=true'])

    @patch('smarter.services.pdf._get_archive_name')
    @patch('smarter.services.pdf._start_bulk')
    @patch('smarter.services.pdf._create_pdf_merge_tasks')
    @patch('smarter.services.pdf._create_pdf_generate_tasks')
    @patch('smarter.services.pdf._get_school_name')
    @patch('smarter.services.pdf.register_file')
    @patch('smarter.services.pdf._create_urls_by_student_guid')
    @patch('smarter.services.pdf.generate_isr_report_path_by_student_guid')
    @patch('smarter.services.pdf._create_student_guids')
    @patch('smarter.services.pdf.authenticated_userid')
    def test_get_bulk_pdf_content(self, mock_authenticated_userid, mock_create_student_guids, mock_generate_isr_report_path_by_student_guid,
                                  mock_create_urls_by_student_guid, mock_register_file, mock_get_school_name, mock_create_pdf_generate_tasks,
                                  mock_create_pdf_merge_tasks, mock_start_bulk, mock_get_archive_name):
        mock_authenticated_userid.get_uid.return_value = ''
        mock_create_student_guids.return_value = '', ''
        mock_generate_isr_report_path_by_student_guid.return_value = ''
        mock_create_urls_by_student_guid.return_value = ''
        mock_register_file.return_value = '', 'http://foo.com/abc/hello'
        mock_get_school_name.return_value = ''
        mock_create_pdf_generate_tasks.return_value = ''
        mock_create_pdf_merge_tasks.return_value = ''
        mock_start_bulk.return_value = ''
        mock_get_archive_name.return_value = 'archive_file.pdf'
        pdf_base_dir = '/foo1'
        base_url = 'http://foo.com/abc'
        cookie_value = 'abc'
        cookie_name = 'efg'
        subprocess_timeout = 10
        student_guids = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        grades = 3
        state_code = 'NC'
        district_guid = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        school_guid = 'a-b-c'
        asmt_type = AssessmentType.SUMMATIVE
        asmt_year = None
        effective_date = '20150401'
        lang = 'en'
        is_grayscale = False
        always_generate = False
        celery_timeout = 5
        params = {}
        response = get_bulk_pdf_content(pdf_base_dir, base_url, cookie_value, cookie_name, subprocess_timeout, student_guids, grades, state_code, district_guid, school_guid, asmt_type, asmt_year, effective_date, lang, is_grayscale, always_generate, celery_timeout, params)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body[Constants.FILENAME], 'archive_file.pdf')
        self.assertEqual(body[Constants.DOWNLOAD_URL], 'http://foo.com/abc/hello')

    @patch('smarter.services.pdf.get_bulk_pdf_content')
    def test_get_pdf_content_for_bulk(self, mock_get_bulk_pdf_content):
        mock_get_bulk_pdf_content.return_value = 'return from get_bulk_pdf_content'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        params = {Constants.STUDENTGUID: ['a', 'b'], Constants.ASMTTYPE: 'SUMMATIVE', Constants.ASMTYEAR: '2015'}
        response = get_pdf_content(params)
        self.assertEqual('return from get_bulk_pdf_content', response)

    @patch('smarter.services.pdf._has_context_for_pdf_request')
    def test__create_urls_by_student_guid_Access_Denied(self, mock_has_context_for_pdf_request):
        mock_has_context_for_pdf_request.return_value = False
        self.assertRaises(ForbiddenError, _create_urls_by_student_guid, [], None, None, {})

    def test_create_pdf_generate_tasks(self):
        cookie_value = 'a'
        cookie_name = 'b'
        is_grayscale = False
        always_generate = False
        files_by_guid = {}
        urls_by_guid = {'a': 'c'}
        tasks = _create_pdf_generate_tasks(cookie_value, cookie_name, is_grayscale, always_generate, files_by_guid, urls_by_guid)
        self.assertEqual(0, len(tasks))
        files_by_guid = {'a': 'b'}
        tasks = _create_pdf_generate_tasks(cookie_value, cookie_name, is_grayscale, always_generate, files_by_guid, urls_by_guid)
        self.assertEqual(1, len(tasks))
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
