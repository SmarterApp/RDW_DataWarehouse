__author__ = 'ablum'

import tempfile
from unittest.mock import patch
from unittest.mock import ANY

from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.registry import Registry
from beaker.cache import CacheManager, cache_managers
from beaker.util import parse_cache_config_options
from pyramid.security import Allow

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edextract.celery import setup_celery
from edauth.tests.test_helper.create_session import create_test_session
from smarter_common.security.constants import RolesConstants
from smarter.extracts.constants import Constants as Extract
from smarter.reports.helpers.constants import Constants
import edauth
from edauth.security.user import User
from edcore.security.tenant import set_tenant_map
from edextract.tasks.constants import Constants as TaskConstants, ExtractionDataType
from smarter.extracts.student_reg_processor import _create_task_info, process_extraction_request, _get_extract_file_path


class TestStudentRegProcessor(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.reg = Registry()
        self.__work_zone_dir = tempfile.TemporaryDirectory()
        self.reg.settings = {'extract.work_zone_base_dir': '/tmp/work_zone',
                             'extract.available_grades': '3,4,5,6,7,8,11',
                             'hpz.file_upload_base_url': 'http://somehost:82/files'}
        settings = {'extract.celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.SRS_EXTRACTS, ('view', 'logout')),
                         (Allow, RolesConstants.SRC_EXTRACTS, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        dummy_session = create_test_session([RolesConstants.SRS_EXTRACTS, RolesConstants.SRC_EXTRACTS])
        self.__config.testing_securitypolicy(dummy_session.get_user())
        set_tenant_map({get_unittest_tenant_name(): 'NC'})

    def tearDown(self):
        # reset the registry
        testing.tearDown()
        cache_managers.clear()

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    @patch('smarter.extracts.student_reg_processor.compile_query_to_sql_text')
    @patch('smarter.extracts.student_reg_processor.student_reg_statistics.get_headers')
    @patch('smarter.extracts.student_reg_processor.student_reg_statistics.get_academic_year_query')
    @patch('smarter.extracts.student_reg_processor.student_reg_statistics.get_match_id_query')
    def test__create_task_info_statistics(self, util_patch, header_patch, aquery_patch, mquery_patch):
        dummy_headers = ('H1', 'H2')

        util_patch.return_value = ''
        header_patch.return_value = dummy_headers
        aquery_patch.return_value = ''
        mquery_patch.return_value = ''

        extract_params = {TaskConstants.STATE_CODE: "NC",
                          TaskConstants.ACADEMIC_YEAR: 2015,
                          Extract.REPORT_TYPE: 'studentRegistrationStatistics',
                          TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_STATISTICS}

        user = User()
        results = _create_task_info("request_id", user, 'tenant', extract_params)

        self.assertEqual(len(results), 8)
        self.assertEqual(2, len(results[TaskConstants.TASK_QUERIES]))
        self.assertEquals('StudentRegistrationStatisticsReportCSV', results[TaskConstants.EXTRACTION_DATA_TYPE])

    @patch('smarter.extracts.student_reg_processor.compile_query_to_sql_text')
    @patch('smarter.extracts.student_reg_processor.student_reg_completion.get_headers')
    @patch('smarter.extracts.student_reg_processor.student_reg_completion.get_academic_year_query')
    @patch('smarter.extracts.student_reg_processor.student_reg_completion.get_assessment_query')
    def test__create_task_info_completion(self, amstquery_patch, aquery_patch, header_patch, util_patch):
        dummy_headers = ('H1', 'H2')

        util_patch.return_value = ''
        header_patch.return_value = dummy_headers
        aquery_patch.return_value = ''
        amstquery_patch.return_value = ''

        extract_params = {TaskConstants.STATE_CODE: "NC",
                          TaskConstants.ACADEMIC_YEAR: 2015,
                          Extract.REPORT_TYPE: 'studentAssessmentCompletion',
                          TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_COMPLETION}

        user = User()
        results = _create_task_info("request_id", user, 'tenant', extract_params)

        self.assertEqual(8, len(results))
        self.assertEquals(dummy_headers, results[TaskConstants.CSV_HEADERS])
        self.assertEqual(2, len(results[TaskConstants.TASK_QUERIES]))
        self.assertEquals('StudentAssessmentCompletionReportCSV', results[TaskConstants.EXTRACTION_DATA_TYPE])

    def test__get_extract_file_path(self):
        extract_params = {TaskConstants.STATE_CODE: "NC",
                          TaskConstants.ACADEMIC_YEAR: 2015,
                          Extract.REPORT_TYPE: ['studentRegistrationStatistics'],
                          TaskConstants.EXTRACTION_DATA_TYPE: ExtractionDataType.SR_STATISTICS}

        result = _get_extract_file_path("requestId", "tenant", extract_params)

        self.assertIn('.csv', result)
        self.assertIn('requestId', result)
        self.assertIn('tenant', result)
        self.assertIn('NC', result)

    @patch('smarter.extracts.student_reg_processor.start_extract')
    @patch('smarter.extracts.student_reg_processor._create_task_info')
    @patch('smarter.extracts.student_reg_processor.register_file')
    def test_process_async_extraction_request(self, register_file_patch, task_info, mock_start_extract):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        dummy_task_info = {'extraction_data_type': 'StudentRegistrationStatisticsReportCSV'}
        task_info.return_value = dummy_task_info
        params = {Constants.STATECODE: 'NC',
                  Constants.ACADEMIC_YEAR: 2015,
                  Extract.EXTRACTTYPE: 'studentRegistrationStatistics'}

        response = process_extraction_request(params)

        self.assertIn('.zip', response['fileName'])
        self.assertEqual(response['tasks'][0]['status'], 'ok')
        self.assertEqual(response['tasks'][0][Constants.ACADEMIC_YEAR], 2015)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response['download_url'])
        self.assertTrue(mock_start_extract.called)
