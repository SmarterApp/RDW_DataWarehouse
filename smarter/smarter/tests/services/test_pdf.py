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
from smarter.services.pdf import sync_pdf_service, async_pdf_service, send_pdf_request, \
    get_pdf_content, _has_context_for_pdf_request, _get_school_name, _get_student_ids, _get_archive_name, \
    _get_merged_pdf_name, _create_student_ids, get_single_pdf_content, \
    _create_student_pdf_url, _create_pdf_merge_tasks, \
    _create_urls_by_student_id, get_bulk_pdf_content,\
    _create_pdf_generate_tasks, _create_cover_sheet_generate_tasks, _create_pdf_cover_merge_tasks,\
    _get_cover_sheet_name, async_pdf_service
from edapi.exceptions import InvalidParameterError, ForbiddenError
from services.celery import setup_celery
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_id
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
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


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
        self.assertRaises(EdApiHTTPPreconditionFailed, sync_pdf_service, DummyValueError())

    def test_sync_pdf_service_post_invalid_param(self):
        self.__request.json_body = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, sync_pdf_service, self.__request)

    def test_sync_pdf_service_no_context(self):
        self.__request.method = 'POST'
        self.__request.json_body = {Constants.STUDENTGUID: ['19489898-d469-41e2-babc-265ecbab2337'],
                                    Constants.STATECODE: 'NC',
                                    Constants.ASMTTYPE: AssessmentType.SUMMATIVE,
                                    Constants.EFFECTIVEDATE: 20160404}

        self.assertRaises(EdApiHTTPForbiddenAccess, sync_pdf_service, None, self.__request)

    def test_sync_pdf_service(self):
        self.__request.method = 'GET'
        studentId = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        self.__request.GET = {Constants.STUDENTGUID: [studentId],
                              Constants.STATECODE: 'NC',
                              Constants.ASMTTYPE: AssessmentType.SUMMATIVE,
                              Constants.EFFECTIVEDATE: 20160404}
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_id('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_ids=studentId, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentId])
        with open(pdf_file[studentId], 'w') as file:
            file.write('%PDF-1.4')
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        response = sync_pdf_service(None, self.__request)
        self.assertEqual(response.content_type, Constants.APPLICATION_PDF)

    def test_async_pdf_service_invalid_param(self):
        self.__request.GET = {}
        self.assertRaises(EdApiHTTPPreconditionFailed, async_pdf_service, self.__request)

    def test_async_pdf_service_invalid_report_name(self):
        self.__request.GET = {}
        self.__request.matchdict[Constants.REPORT] = 'newReport'
        self.assertRaises(EdApiHTTPPreconditionFailed, async_pdf_service, self.__request)

    def test_async_pdf_service_no_context(self):
        self.__request.method
        self.__request.GET = {Constants.STUDENTGUID: '19489898-d469-41e2-babc-265ecbab2337', Constants.STATECODE: 'NC', Constants.EFFECTIVEDATE: 20160404}
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'

        self.assertRaises(EdApiHTTPForbiddenAccess, sync_pdf_service, None, self.__request)

    def test_get_pdf_valid_params(self):
        studentId = 'a016a4c1-5aca-4146-a85b-ed1172a01a4d'
        self.__request.GET[Constants.STUDENTGUID] = studentId
        self.__request.GET[Constants.STATECODE] = 'NC'
        self.__request.GET[Constants.EFFECTIVEDATE] = 20160404
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_id('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_ids=studentId, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentId])
        with open(pdf_file[studentId], 'w') as file:
            file.write('%PDF-1.4')
        # Override the wkhtmltopdf command
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        response = sync_pdf_service(None, self.__request)
        self.assertIsInstance(response, Response)
        self.assertIsNotNone(response.body)
        self.assertEqual(response.content_type, Constants.APPLICATION_PDF)

    def test_send_pdf_request(self):
        studentId = "a016a4c1-5aca-4146-a85b-ed1172a01a4d"
        params = {}
        params[Constants.STUDENTGUID] = studentId
        params[Constants.STATECODE] = 'NC'
        params[Constants.EFFECTIVEDATE] = 20160404
        params['dummy'] = 'dummy'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        # prepare empty file
        pdf_file = generate_isr_report_path_by_student_id('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_ids=studentId, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentId])
        with open(pdf_file[studentId], 'w') as file:
            file.write('%PDF-1.4')
        response = send_pdf_request(params, sync=True)
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
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params, sync=True)

    def test_get_pdf_content_with_missing_student_id(self):
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
        self.assertRaises(ForbiddenError, get_pdf_content, params, sync=True)

    def test_has_context_for_pdf_request(self):
        student_id = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        has_context = _has_context_for_pdf_request('NC', student_id)
        self.assertTrue(has_context)

    def test_has_context_for_pdf_request_with_no_context(self):
        student_id = 'invalid'
        has_context = _has_context_for_pdf_request('NC', student_id)
        self.assertFalse(has_context)

    def test_send_pdf_request_with_always_generate_flag(self):
        self.__config.registry.settings['pdf.always_generate'] = 'True'
        studentId = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        params = {}
        params[Constants.STUDENTGUID] = studentId
        params[Constants.STATECODE] = 'NC'
        params['dummy'] = 'dummy'
        params[Constants.EFFECTIVEDATE] = 20160404
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        self.__request.cookies = {'edware': '123'}
        services.tasks.pdf.pdf_procs = get_cmd()
        # prepare empty file to mimic a pdf was generated
        pdf_file = generate_isr_report_path_by_student_id('NC', "20160404", pdf_report_base_dir=self.__temp_dir, student_ids=studentId, asmt_type=AssessmentType.SUMMATIVE)
        prepare_path(pdf_file[studentId])
        with open(pdf_file[studentId], 'w') as file:
            file.write('%PDF-1.4')
        self.assertRaises(EdApiHTTPInternalServerError, send_pdf_request, params, sync=True)

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

    def test_get_student_ids(self):
        guids = _get_student_ids('NC', '229', '939', AssessmentType.SUMMATIVE, {}, '2016', '20160404', '7')
        self.assertEqual(len(guids), 8)

    def test_get_student_ids_males(self):
        guids = _get_student_ids('NC', '229', '939', AssessmentType.SUMMATIVE, {'sex': ['male']}, '2016', '20160404', '7')
        self.assertEqual(len(guids), 4)

    def test_get_student_ids_group1(self):
        guids = _get_student_ids('NC', '229', '939', AssessmentType.SUMMATIVE, {'group1Id': ['d20236e0-eb48-11e3-ac10-0800200c9a66']}, '2016', '20160404', '7')
        self.assertEqual(len(guids), 5)

    def test_get_student_ids_group2(self):
        guids = _get_student_ids('NC', '229', '939', AssessmentType.SUMMATIVE, {'group2Id': ['ee7bcbb0-eb48-11e3-ac10-0800200c9a66']}, '2016', '20160404', '7')
        self.assertEqual(len(guids), 6)

    def test_get_student_ids_alphabetical(self):
        recs = _get_student_ids('NC', '229', '939', AssessmentType.SUMMATIVE, {}, '2016', '20160404', '7')
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

    def test_create_student_ids_by_guids(self):
        all_guids, guids_by_grade = _create_student_ids(['c799b218-0bfb-413d-9ec1-684cde99851d',
                                                        '115f7b10-9e18-11e2-9e96-0800200c9a66'], ['8'], 'NC', '229',
                                                        '939', AssessmentType.SUMMATIVE, '2016', '20160404', {})
        self.assertEqual(len(all_guids), 2)
        self.assertIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['8']), 2)

    def test_create_student_ids_by_grade(self):
        all_guids, guids_by_grade = _create_student_ids(None, ['7', '8'], 'NC', '229', '939', AssessmentType.SUMMATIVE,
                                                        '2016', '20160404', {})
        self.assertEqual(len(all_guids), 10)
        self.assertIn('7', guids_by_grade)
        self.assertIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['7']), 8)
        self.assertEqual(len(guids_by_grade['8']), 2)

    def test_create_student_ids_by_grade_group(self):
        all_guids, guids_by_grade = _create_student_ids(None, ['7', '8'], 'NC', '229', '939', AssessmentType.SUMMATIVE,
                                                        '2016', '20160404',
                                                        {'group1Id': ['d20236e0-eb48-11e3-ac10-0800200c9a66']})
        self.assertEqual(len(all_guids), 5)
        self.assertIn('7', guids_by_grade)
        self.assertNotIn('8', guids_by_grade)
        self.assertEqual(len(guids_by_grade['7']), 5)

    def test_create_student_ids_by_guids_no_students(self):
        self.assertRaises(InvalidParameterError, _create_student_ids, [], None, 'NC', '229', '939', AssessmentType.SUMMATIVE,
                          '2016', '20160404', {})

    def test_create_student_ids_by_grade_no_students(self):
        self.assertRaises(InvalidParameterError, _create_student_ids, None, ['7'], 'NC', '229', '939', AssessmentType.SUMMATIVE,
                          '2016', '20160404', {'sex': ['not_stated']})

    @patch('smarter.services.pdf.get.apply_async')
    def test_get_single_pdf_content(self, mock_get):
        mock_get.return_value.get.return_value = 'BIG PDF CONTENT STUFF'.encode()
        response = get_single_pdf_content('/tmp', 'localhost/', '123', 'edware', 30, 'NC', '2016', '20160404', AssessmentType.SUMMATIVE,
                                          'a629ca88-afe6-468c-9dbb-92322a284602', 'en', False, False, 30, {}, 'single_pdf')
        self.assertEqual(response.status_code, 200)

    @patch('smarter.services.pdf.get')
    def test_get_single_pdf_content_bad_effective_date(self, mock_get):
        mock_get.return_value = None
        self.assertRaises(APINotFoundException, get_single_pdf_content, '/tmp', 'localhost/', '123', 'edware', 30, 'NC',
                          '2016', '20160304', AssessmentType.SUMMATIVE, 'a629ca88-afe6-468c-9dbb-92322a284602', 'en',
                          False, False, 30, {}, 'single_pdf')

    @patch('smarter.services.pdf.get')
    def test_get_single_pdf_content_bad_student_id(self, mock_get):
        mock_get.return_value = None
        self.assertRaises(APIForbiddenError, get_single_pdf_content, '/tmp', 'localhost/', '123', 'edware', 30, 'NC',
                          '2016', '20160404', AssessmentType.SUMMATIVE, 'a629ca88-afe6-468c-9dbb', 'en', False, False,
                          30, {}, 'single_pdf')

    def test_create_student_pdf_url(self):
        student_id = '1-2-3-4-5'
        base_url = 'http://foo.com/foo'
        params = {}
        result = _create_student_pdf_url(student_id, base_url, params)
        self.assertIn(result, ['http://foo.com/foo?pdf=true&studentId=1-2-3-4-5', 'http://foo.com/foo?studentId=1-2-3-4-5&pdf=true'])
        params = {'abc': 'ef'}
        result = _create_student_pdf_url(student_id, base_url, params)
        self.assertTrue('abc=ef' in result)

    def test_create_pdf_merge_tasks_no_guid(self):
        pdf_base_dir = '/base'
        directory_for_merged = '/merged'
        directory_for_covers = '/covers'
        guids_by_grade = []
        files_by_guid = {'a5ddfe12-740d-4487-9179-de70f6ac33be': '/foo/abc.pdf'}
        school_name = 'schoolname here'
        lang = 'en'
        is_grayscale = None
        tasks, paths, counts = _create_pdf_merge_tasks(pdf_base_dir, directory_for_merged, guids_by_grade, files_by_guid, school_name, lang, is_grayscale)
        self.assertEqual(0, len(tasks))
        self.assertEqual(0, len(paths))
        self.assertEqual(0, len(counts))
        guids_by_grade = {'3': 'a5ddfe12-740d-4487-9179-de70f6ac33be'}
        tasks, paths, counts = _create_pdf_merge_tasks(pdf_base_dir, directory_for_merged, guids_by_grade, files_by_guid, school_name, lang, is_grayscale)
        self.assertEqual(1, len(tasks))
        self.assertEqual(1, len(paths))
        self.assertEqual(1, len(counts))

    def test_create_pdf_merge_tasks_with_guids(self):
        pdf_base_dir = '/foo'
        directory_for_merged = '/merged'
        guids_by_grade = {'2': ['1-2-3-4', 'a-b-c-d'], '3': '4-3-2-1'}
        files_by_guid = {'1-2-3-4': '/foo/1.pdf', 'a-b-c-d': '/foo/2.pdf', '4-3-2-1': '/foo/3.pdf'}
        school_name = 'Apple School'
        lang = 'en'
        is_grayscale = False
        tasks, paths, counts = _create_pdf_merge_tasks(pdf_base_dir, directory_for_merged, guids_by_grade, files_by_guid, school_name, lang, is_grayscale)
        self.assertEqual(2, len(paths))
        self.assertEqual(2, len(counts))
        self.assertIn('2', counts)
        self.assertIn('3', counts)
        self.assertEqual(2, counts['2'])
        self.assertEqual(1, counts['3'])
        self.assertEqual(2, len(tasks))

    def test_create_cover_sheet_generate_tasks(self):
        cookie_val = 'jsdfhiaewf90ahfa;kdfja;weiofaw'
        cookie_name = 'edware'
        is_grayscale = True
        school_name = 'The Great School of Magnificent Grandeur'
        user_name = 'Principal Pigwilly'
        directory_for_covers = '/covers'
        merged_by_grade = {'3': '/merged/3.pdf', '4': '/merged/4.pdf', '5': '/merged/5.pdf'}
        student_count_by_grade = {'3': 7, '4': 9, '5': 15}
        tasks, sheets = _create_cover_sheet_generate_tasks(cookie_val, cookie_name, is_grayscale, school_name,
                                                           user_name, directory_for_covers, merged_by_grade,
                                                           student_count_by_grade)
        self.assertEqual(3, len(tasks))
        self.assertEqual(3, len(sheets))

    def test_create_cover_sheet_generate_tasks_no_generated(self):
        cookie_val = 'jsdfhiaewf90ahfa;kdfja;weiofaw'
        cookie_name = 'edware'
        is_grayscale = True
        school_name = 'The Great School of Magnificent Grandeur'
        user_name = 'Principal Pigwilly'
        directory_for_covers = '/covers'
        merged_by_grade = None
        student_count_by_grade = {'3': 7, '4': 9, '5': 15}
        tasks, sheets = _create_cover_sheet_generate_tasks(cookie_val, cookie_name, is_grayscale, school_name,
                                                           user_name, directory_for_covers, merged_by_grade,
                                                           student_count_by_grade)
        self.assertEqual(0, len(tasks))
        self.assertEqual(0, len(sheets))

    def test_create_pdf_cover_merge_tasks(self):
        merged_pdfs_by_grade = {'3': '/meged/3.pdf', '4': '/merged/4.pdf'}
        cover_sheets_by_grade = {'3': '/covers/3.pdf', '4': '/covers/4.pdf'}
        directory_to_archive = '/archive'
        pdf_base_dir = '/pdf'
        tasks = _create_pdf_cover_merge_tasks(merged_pdfs_by_grade, cover_sheets_by_grade, directory_to_archive,
                                              pdf_base_dir)
        self.assertEqual(2, len(tasks))

    def test_create_pdf_cover_merge_tasks_no_merged(self):
        merged_pdfs_by_grade = None
        cover_sheets_by_grade = None
        directory_to_archive = '/archive'
        pdf_base_dir = '/pdf'
        tasks = _create_pdf_cover_merge_tasks(merged_pdfs_by_grade, cover_sheets_by_grade, directory_to_archive,
                                              pdf_base_dir)
        self.assertEqual(0, len(tasks))

    def test_create_urls_by_student_id(self):
        studentId = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        baseURL = 'http://foo.com/abc'
        url = _create_urls_by_student_id(studentId, 'NC', baseURL, {})
        self.assertIn(url['a5ddfe12-740d-4487-9179-de70f6ac33be'], ['http://foo.com/abc?pdf=true&studentId=a5ddfe12-740d-4487-9179-de70f6ac33be',
                                                                    'http://foo.com/abc?studentId=a5ddfe12-740d-4487-9179-de70f6ac33be&pdf=true'])

    def test_get_cover_sheet_name(self):
        name = _get_cover_sheet_name('7')
        self.assertEqual('cover_sheet_grade_7.pdf', name)

    @patch('smarter.services.pdf._get_archive_name')
    @patch('smarter.services.pdf._get_cover_sheet_name')
    @patch('smarter.services.pdf._start_bulk')
    @patch('smarter.services.pdf._create_cover_sheet_generate_tasks')
    @patch('smarter.services.pdf._create_pdf_merge_tasks')
    @patch('smarter.services.pdf._create_pdf_generate_tasks')
    @patch('smarter.services.pdf._get_school_name')
    @patch('smarter.services.pdf.register_file')
    @patch('smarter.services.pdf._create_urls_by_student_id')
    @patch('smarter.services.pdf.generate_isr_report_path_by_student_id')
    @patch('smarter.services.pdf._create_student_ids')
    @patch('smarter.services.pdf.authenticated_userid')
    def test_get_bulk_pdf_content(self, mock_authenticated_userid, mock_create_student_ids, mock_generate_isr_report_path_by_student_id,
                                  mock_create_urls_by_student_id, mock_register_file, mock_get_school_name, mock_create_pdf_generate_tasks,
                                  mock_create_pdf_merge_tasks, mock_create_cover_sheet_generate_tasks, mock_start_bulk,
                                  mock_get_cover_sheet_name, mock_get_archive_name):
        mock_authenticated_userid.get_uid.return_value = ''
        mock_create_student_ids.return_value = '', ''
        mock_generate_isr_report_path_by_student_id.return_value = ''
        mock_create_urls_by_student_id.return_value = ''
        mock_register_file.return_value = '', 'http://foo.com/abc/hello'
        mock_get_school_name.return_value = ''
        mock_create_pdf_generate_tasks.return_value = ''
        mock_create_pdf_merge_tasks.return_value = '', '', ''
        mock_create_cover_sheet_generate_tasks.return_value = '', ''
        mock_start_bulk.return_value = ''
        mock_get_cover_sheet_name.return_value = 'cover_sheet_grade_3.pdf'
        mock_get_archive_name.return_value = 'archive_file.pdf'
        pdf_base_dir = '/foo1'
        base_url = 'http://foo.com/abc'
        subprocess_timeout = 10
        student_ids = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        grades = 3
        state_code = 'NC'
        district_id = 'a5ddfe12-740d-4487-9179-de70f6ac33be'
        school_id = 'a-b-c'
        asmt_type = AssessmentType.SUMMATIVE
        asmt_year = None
        effective_date = '20150401'
        lang = 'en'
        is_grayscale = False
        always_generate = False
        celery_timeout = 5
        params = {}
        settings = {}
        settings['cache.regions'] = 'public.data, session'
        settings['cache.type'] = 'memory'
        settings['auth.policy.secret'] = 'secret'
        settings['auth.policy.cookie_name'] = 'myName'
        settings['auth.policy.hashalg'] = 'sha1'
        settings['batch.user.session.timeout'] = 10777700
        CacheManager(**parse_cache_config_options(settings))
        component.provideUtility(SessionBackend(settings), ISessionBackend)
        response = get_bulk_pdf_content(settings, pdf_base_dir, base_url, subprocess_timeout, student_ids, grades, state_code, district_id, school_id, asmt_type, asmt_year, effective_date, lang, is_grayscale, always_generate, celery_timeout, params)
        body = json.loads(response.body.decode('utf-8'))
        self.assertEqual(body[Constants.FILES][0][Constants.FILENAME], 'archive_file.pdf')
        self.assertEqual(body[Constants.FILES][0][Constants.DOWNLOAD_URL], 'http://foo.com/abc/hello')

    @patch('smarter.services.pdf.get_bulk_pdf_content')
    def test_get_pdf_content_for_bulk(self, mock_get_bulk_pdf_content):
        mock_get_bulk_pdf_content.return_value = 'return from get_bulk_pdf_content'
        self.__request.matchdict[Constants.REPORT] = 'indivStudentReport.html'
        params = {Constants.STUDENTGUID: ['a', 'b'], Constants.ASMTTYPE: 'SUMMATIVE', Constants.ASMTYEAR: '2015'}
        response = get_pdf_content(params)
        self.assertEqual('return from get_bulk_pdf_content', response)

    @patch('smarter.services.pdf._has_context_for_pdf_request')
    def test__create_urls_by_student_id_Access_Denied(self, mock_has_context_for_pdf_request):
        mock_has_context_for_pdf_request.return_value = False
        self.assertRaises(ForbiddenError, _create_urls_by_student_id, [], None, None, {})

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
