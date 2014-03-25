__author__ = 'tshewchuk'

"""
Module containing Student Registration report generator unit tests.
"""

import os
import tempfile
import shutil
import csv

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, UnittestEdcoreDBConnection,
                                                            get_unittest_tenant_name)
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants


class TestStudentRegReportGenerator(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self._tenant = get_unittest_tenant_name()
        self.query = 'SELECT * FROM student_reg WHERE academic_year == 2014'
        self.statistics_headers = ['State', 'District', 'School', 'Category', 'Value', 'AY2013 Count', 'AY2013 Percent of Total',
                                   'AY2014 Count', 'AY2014 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                   'Change in Percent of Total', 'AY2014 Matched IDs to AY2013 Count', 'AY2014 Matched IDs Percent of AY2013 count']
        self.completion_headers = ['State', 'District', 'School', 'Grade', 'Category', 'Value', 'Assessment Subject',
                                   'Assessment Type', 'Assessment Date', 'Academic Year', 'Count of Students Registered',
                                   'Count of Students Assessed', 'Percent of Students Assessed']

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    def test_generate_statistics_report_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.ACADEMIC_YEAR: 2014,
                        TaskConstants.TASK_QUERY: self.query,
                        TaskConstants.CSV_HEADERS: self.statistics_headers}
        generate_statistics_report(self._tenant, output, task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 1)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Category', 'Value', 'AY2013 Count', 'AY2013 Percent of Total',
                                       'AY2014 Count', 'AY2014 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                       'Change in Percent of Total', 'AY2014 Matched IDs to AY2013 Count', 'AY2014 Matched IDs Percent of AY2013 count'])

    def test_generate_completion_report_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_comp.csv')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.ACADEMIC_YEAR: 2014,
                        TaskConstants.TASK_QUERY: self.query,
                        TaskConstants.CSV_HEADERS: self.completion_headers}
        generate_completion_report(self._tenant, output, task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 1)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Grade', 'Category', 'Value', 'Assessment Subject',
                                       'Assessment Type', 'Assessment Date', 'Academic Year', 'Count of Students Registered',
                                       'Count of Students Assessed', 'Percent of Students Assessed'])
