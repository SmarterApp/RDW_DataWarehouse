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
from edextract.data_extract_generation.student_reg_report_generator import (generate_statistics_report_data, generate_statistics_report,
                                                                            generate_completion_report_data, generate_completion_report,
                                                                            get_sr_tenant_data_for_academic_year)
from edextract.status.constants import Constants
from edextract.tasks.student_reg_constants import Constants as TaskConstants


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

    def test_generate_statistics_report_data_no_data(self):
        header, data = generate_statistics_report_data(self._tenant, 2014)
        self.assertEqual(header, ('State', 'District', 'School', 'Category', 'Value', 'AY2013 Count', 'AY2013 Percent of Total',
                                  'AY2014 Count', 'AY2014 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                  'Change in Percent of Total', 'AY2014 Matched IDs to AY2013 Count', 'AY2014 Matched IDs Percent of AY2013 count'))
        self.assertEquals(data, [])

    def test_generate_completion_report_data_no_data(self):
        header, data = generate_completion_report_data(self._tenant, 2014)
        self.assertEquals(data, [])
        self.assertEqual(header, ('State', 'District', 'School', 'Grade', 'Category', 'Value', 'Assessment Subject',
                                  'Assessment Type', 'Assessment Date', 'Academic Year', 'Count of Students Registered',
                                  'Count of Students Assessed', 'Percent of Students Assessed'))

    def test_generate_statistics_report_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.ACADEMIC_YEAR: 2014}
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

    def get_sr_tenant_data_for_academic_year(self):
        data = get_sr_tenant_data_for_academic_year(self._tenant, 2014)
        self.assertEquals([], data)
