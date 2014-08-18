__author__ = 'tshewchuk'

"""
Module containing Student Registration report generator unit tests.
"""

import os
import tempfile
import shutil
from unittest.mock import patch

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, ExtractionDataType, QueryType


class TestStudentRegReportGenerator(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self._tenant = get_unittest_tenant_name()
        self.task_info = {Constants.TASK_ID: '01',
                          Constants.CELERY_TASK_ID: '02',
                          Constants.REQUEST_GUID: '03'}

    @classmethod
    def setUpClass(cls):
        here = os.path.abspath(os.path.dirname(__file__))
        resources_dir = os.path.abspath(os.path.join(os.path.join(here, 'resources')))
        Unittest_with_edcore_sqlite.setUpClass(resources_dir=resources_dir)
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    @patch('edextract.data_extract_generation.student_reg_report_generator._generate_statistics_report_data')
    @patch('edextract.data_extract_generation.student_reg_report_generator.write_csv')
    def test_generate_statistics_report_success(self, mock_write_csv, mock__generate_statistics_report_data):
        output = 'stureg_stat_1_yr.csv'
        academic_year = 2014
        current_year = str(academic_year)
        academic_year_query = 'AYQ {current_year}'.format(current_year=current_year)
        match_id_query = 'MIQ {current_year}'.format(current_year=current_year)
        header = ['Statistics Report', 'AY{current_year} Count'.format(current_year=current_year)]
        data = (['report 1', '100'], ['report 2', '200'])
        queries = {QueryType.QUERY: academic_year_query, QueryType.MATCH_ID_QUERY: match_id_query}
        extract_args = {TaskConstants.ACADEMIC_YEAR: academic_year, TaskConstants.TASK_QUERIES: queries, TaskConstants.CSV_HEADERS: header}
        mock_write_csv.return_value = None
        mock__generate_statistics_report_data.return_value = data

        generate_statistics_report(self._tenant, output, self.task_info, extract_args)

        mock__generate_statistics_report_data.assert_called_with(self._tenant, academic_year, queries)
        mock_write_csv.assert_called_with(output, data, header=header)

    @patch('edextract.data_extract_generation.student_reg_report_generator._generate_completion_report_data')
    @patch('edextract.data_extract_generation.student_reg_report_generator.write_csv')
    def test_generate_completion_report_success(self, mock_write_csv, mock__generate_completion_report_data):
        output = 'stureg_stat_1_yr.csv'
        academic_year = 2014
        current_year = str(academic_year)
        academic_year_query = 'AYQ {current_year}'.format(current_year=current_year)
        header = ['Completion Report', 'AY{current_year} Count'.format(current_year=current_year)]
        data = (['report 1', '100'], ['report 2', '200'])
        queries = {QueryType.QUERY: academic_year_query}
        extract_args = {TaskConstants.ACADEMIC_YEAR: academic_year, TaskConstants.TASK_QUERIES: queries, TaskConstants.CSV_HEADERS: header}
        mock_write_csv.return_value = None
        mock__generate_completion_report_data.return_value = data

        generate_completion_report(self._tenant, output, self.task_info, extract_args)

        mock__generate_completion_report_data.assert_called_with(self._tenant, academic_year, queries)
        mock_write_csv.assert_called_with(output, data, header=header)
