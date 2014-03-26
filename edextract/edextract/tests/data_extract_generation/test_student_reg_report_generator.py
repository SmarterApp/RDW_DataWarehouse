__author__ = 'tshewchuk'

"""
Module containing Student Registration report generator unit tests.
"""

import os
import tempfile
import shutil
import csv

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants


class TestStudentRegReportGenerator(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self._tenant = get_unittest_tenant_name()

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
        extract_args = {TaskConstants.ACADEMIC_YEAR: 2015}
        generate_statistics_report(self._tenant, output, task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 6)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Category', 'Value', 'AY2014 Count', 'AY2014 Percent of Total',
                                       'AY2015 Count', 'AY2015 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                       'Change in Percent of Total', 'AY2015 Matched IDs to AY2014 Count', 'AY2015 Matched IDs Percent of AY2014 count'])
        self.assertEqual(csv_data[1], ['Dummy State', 'ALL', 'ALL', 'Total', 'Total', '9', '100.0', '9', '100.0', '0', '0.0', '0.0'])
        self.assertEqual(csv_data[2], ['Dummy State', 'Podunk South District', 'ALL', 'Total', 'Total', '4', '100.0', '5', '100.0', '1', '25.0', '0.0'])
        self.assertEqual(csv_data[3], ['Dummy State', 'Podunk South District', "Thomson's Gazelle High", 'Total', 'Total', '4', '100.0', '5', '100.0', '1', '25.0', '0.0'])
        self.assertEqual(csv_data[4], ['Dummy State', 'West Podunk School District', 'ALL', 'Total', 'Total', '5', '100.0', '4', '100.0', '-1', '-20.0', '0.0'])
        self.assertEqual(csv_data[5], ['Dummy State', 'West Podunk School District', 'Saddleback Tortoise High', 'Total', 'Total', '5', '100.0', '4', '100.0', '-1', '-20.0', '0.0'])

    def test_generate_completion_report_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_comp.csv')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.ACADEMIC_YEAR: 2014}
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
