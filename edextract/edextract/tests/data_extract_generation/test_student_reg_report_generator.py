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
from edextract.tasks.constants import Constants as TaskConstants, ExtractionDataType


class TestStudentRegReportGenerator(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self._tenant = get_unittest_tenant_name()
        self.completion_headers = ['State', 'District', 'School', 'Grade', 'Category', 'Value', 'Assessment Subject',
                                   'Assessment Type', 'Assessment Date', 'Academic Year', 'Count of Students Registered',
                                   'Count of Students Assessed', 'Percent of Students Assessed']
        self.task_info = {Constants.TASK_ID: '01',
                          Constants.CELERY_TASK_ID: '02',
                          Constants.REQUEST_GUID: '03'}

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    def test_generate_statistics_report_one_year_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat_1_yr.csv')
        extract_args = self.construct_extract_args(ExtractionDataType.SR_STATISTICS, 2015, output)
        generate_statistics_report(self._tenant, output, self.task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 16)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Category', 'Value', 'AY2014 Count', 'AY2014 Percent of Total',
                                       'AY2015 Count', 'AY2015 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                       'Change in Percent of Total', 'AY2015 Matched IDs to AY2014 Count', 'AY2015 Matched IDs Percent of AY2014 count'])
        self.assertEqual(csv_data[1], ['Example State', 'ALL', 'ALL', 'Total', 'Total', '0', '', '1217', '100.0', '1217', '', ''])
        self.assertEqual(csv_data[2], ['Example State', 'Holly Tinamou County Schools', 'ALL', 'Total', 'Total', '0', '', '594', '100.0', '594', '', ''])
        self.assertEqual(csv_data[3], ['Example State', 'Holly Tinamou County Schools', 'Basil Caribou Elementary', 'Total', 'Total', '0', '', '89', '100.0', '89', '', ''])
        self.assertEqual(csv_data[4], ['Example State', 'Holly Tinamou County Schools', 'Duck Tityra Sch', 'Total', 'Total', '0', '', '88', '100.0', '88', '', ''])
        self.assertEqual(csv_data[9], ['Example State', 'Kudu Woodcreeper Public Schools', 'ALL', 'Total', 'Total', '0', '', '623', '100.0', '623', '', ''])
        self.assertEqual(csv_data[14], ['Example State', 'Kudu Woodcreeper Public Schools', 'Saltator Kinkajou Elementary', 'Total', 'Total', '0', '', '89', '100.0', '89', '', ''])
        self.assertEqual(csv_data[15], ['Example State', 'Kudu Woodcreeper Public Schools', 'Warbler Serval Middle School', 'Total', 'Total', '0', '', '156', '100.0', '156', '', ''])

    def test_generate_statistics_report_two_years_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat_2_yr.csv')
        extract_args = self.construct_extract_args(ExtractionDataType.SR_STATISTICS, 2016, output)
        generate_statistics_report(self._tenant, output, self.task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 16)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Category', 'Value', 'AY2015 Count', 'AY2015 Percent of Total',
                                       'AY2016 Count', 'AY2016 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                       'Change in Percent of Total', 'AY2016 Matched IDs to AY2015 Count', 'AY2016 Matched IDs Percent of AY2015 count'])
        self.assertEqual(csv_data[1], ['Example State', 'ALL', 'ALL', 'Total', 'Total', '1217', '100.0', '1364', '100.0', '147', '12.08', '0.0'])
        self.assertEqual(csv_data[2], ['Example State', 'Holly Tinamou County Schools', 'ALL', 'Total', 'Total', '594', '100.0', '668', '100.0', '74', '12.46', '0.0'])
        self.assertEqual(csv_data[3], ['Example State', 'Holly Tinamou County Schools', 'Basil Caribou Elementary', 'Total', 'Total', '89', '100.0', '91', '100.0', '2', '2.25', '0.0'])
        self.assertEqual(csv_data[4], ['Example State', 'Holly Tinamou County Schools', 'Duck Tityra Sch', 'Total', 'Total', '88', '100.0', '89', '100.0', '1', '1.14', '0.0'])
        self.assertEqual(csv_data[9], ['Example State', 'Kudu Woodcreeper Public Schools', 'ALL', 'Total', 'Total', '623', '100.0', '696', '100.0', '73', '11.72', '0.0'])
        self.assertEqual(csv_data[14], ['Example State', 'Kudu Woodcreeper Public Schools', 'Saltator Kinkajou Elementary', 'Total', 'Total', '89', '100.0', '91', '100.0', '2', '2.25', '0.0'])
        self.assertEqual(csv_data[15], ['Example State', 'Kudu Woodcreeper Public Schools', 'Warbler Serval Middle School', 'Total', 'Total', '156', '100.0', '233', '100.0', '77', '49.36', '0.0'])

    def test_generate_completion_report_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_comp.csv')
        extract_args = self.construct_extract_args(ExtractionDataType.SR_COMPLETION, 2016, output)
        generate_completion_report(self._tenant, output, self.task_info, extract_args)
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

    def construct_extract_args(self, extraction_type, academic_year, output):
        current_year = str(academic_year)
        previous_year = str(academic_year - 1)
        query = 'SELECT * FROM student_reg WHERE academic_year == {current_year} OR academic_year == {previous_year}'\
            .format(current_year=current_year, previous_year=previous_year)
        headers = self.construct_statistics_headers(academic_year) if extraction_type == ExtractionDataType.SR_STATISTICS \
            else self.completion_headers
        extract_args = {TaskConstants.EXTRACTION_DATA_TYPE: extraction_type,
                        TaskConstants.TASK_TASK_ID: 'task_id',
                        TaskConstants.ACADEMIC_YEAR: academic_year,
                        TaskConstants.TASK_FILE_NAME: output,
                        TaskConstants.TASK_QUERY: query,
                        TaskConstants.CSV_HEADERS: headers
                        }

        return extract_args

    def construct_statistics_headers(self, academic_year):
        current_year = str(academic_year)
        previous_year = str(academic_year - 1)
        statistics_headers = ['State', 'District', 'School', 'Category', 'Value',
                              'AY{previous_year} Count'.format(previous_year=previous_year),
                              'AY{previous_year} Percent of Total'.format(previous_year=previous_year),
                              'AY{current_year} Count'.format(current_year=current_year),
                              'AY{current_year} Percent of Total'.format(current_year=current_year), 'Change in Count',
                              'Percent Difference in Count', 'Change in Percent of Total',
                              'AY{current_year} Matched IDs to AY{previous_year} Count'.format(current_year=current_year, previous_year=previous_year),
                              'AY{current_year} Matched IDs Percent of AY{previous_year} count'.format(current_year=current_year, previous_year=previous_year)]

        return statistics_headers
