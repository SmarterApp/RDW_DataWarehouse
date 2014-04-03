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
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report
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

    def test_generate_statistics_report_one_year_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat_1_yr.csv')
        extract_args = self.construct_extract_args(ExtractionDataType.SR_STATISTICS, 2014, output)
        generate_statistics_report(self._tenant, output, self.task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        #Data has 1 state, 2 districts and 3 schools
        self.assertEqual(len(csv_data), 169)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Category', 'Value', 'AY2013 Count', 'AY2013 Percent of Total',
                                       'AY2014 Count', 'AY2014 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                       'Change in Percent of Total', 'AY2014 Matched IDs to AY2013 Count', 'AY2014 Matched IDs Percent of AY2013 Count'])
        self.assertEqual(csv_data[1], ['Example State', 'ALL', 'ALL', 'Total', 'Total', '', '', '5', '100', '', '', '', '', ''])

    def test_generate_statistics_report_two_years_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat_2_yr.csv')
        extract_args = self.construct_extract_args(ExtractionDataType.SR_STATISTICS, 2015, output)
        generate_statistics_report(self._tenant, output, self.task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        #Data has 1 state, 2 districts and 3 schools
        self.assertEqual(len(csv_data), 169)
        self.assertEqual(csv_data[0], ['State', 'District', 'School', 'Category', 'Value', 'AY2014 Count', 'AY2014 Percent of Total',
                                       'AY2015 Count', 'AY2015 Percent of Total', 'Change in Count', 'Percent Difference in Count',
                                       'Change in Percent of Total', 'AY2015 Matched IDs to AY2014 Count', 'AY2015 Matched IDs Percent of AY2014 Count'])
        self.assertEqual(csv_data[1], ['Example State', 'ALL', 'ALL', 'Total', 'Total', '5', '100', '5', '100', '0', '0', '0', '5', '100'])

    def construct_extract_args(self, extraction_type, academic_year, output):
        current_year = str(academic_year)
        previous_year = str(academic_year - 1)
        academic_year_query = 'SELECT * FROM student_reg WHERE academic_year == {current_year} OR academic_year == {previous_year}'\
            .format(current_year=current_year, previous_year=previous_year)
        match_query = 'SELECT cr.state_code, p.state_code as prev_state_code , cr.state_name, cr.district_guid, p.district_guid as prev_district_guid ,' \
                      'cr.district_name, cr.school_guid, p.school_guid as prev_school_guid , cr.school_name, cr.gender, p.gender as prev_gender , ' \
                      'cr.enrl_grade, p.enrl_grade as prev_enrl_grade , cr.dmg_eth_hsp, p.dmg_eth_hsp as prev_dmg_eth_hsp , cr.dmg_eth_ami, ' \
                      'p.dmg_eth_ami as prev_dmg_eth_ami , cr.dmg_eth_asn, p.dmg_eth_asn as prev_dmg_eth_asn ,cr.dmg_eth_blk, p.dmg_eth_blk as prev_dmg_eth_blk , ' \
                      'cr.dmg_eth_pcf, p.dmg_eth_pcf as prev_dmg_eth_pcf ,cr.dmg_eth_wht, p.dmg_eth_wht as prev_dmg_eth_wht , cr.dmg_prg_iep, ' \
                      'p.dmg_prg_iep as prev_dmg_prg_iep , cr.dmg_prg_lep, p.dmg_prg_lep as prev_dmg_prg_lep ,cr.dmg_prg_504, ' \
                      'p.dmg_prg_504 as prev_dmg_prg_504 , cr.dmg_sts_ecd, p.dmg_sts_ecd as prev_dmg_sts_ecd , cr.dmg_sts_mig, p.dmg_sts_mig as prev_dmg_sts_mig ,' \
                      ' cr.dmg_multi_race, p.dmg_multi_race as prev_dmg_multi_race , cr.academic_year ' \
                      'FROM student_reg cr inner join student_reg p on cr.student_guid = p.student_guid WHERE cr.academic_year == {current_year} AND p.academic_year == {previous_year}'\
            .format(current_year=current_year, previous_year=previous_year)
        headers = self.construct_statistics_headers(academic_year) if extraction_type == ExtractionDataType.SR_STATISTICS \
            else self.completion_headers()
        extract_args = {TaskConstants.EXTRACTION_DATA_TYPE: extraction_type,
                        TaskConstants.TASK_TASK_ID: 'task_id',
                        TaskConstants.ACADEMIC_YEAR: academic_year,
                        TaskConstants.TASK_FILE_NAME: output,
                        TaskConstants.TASK_QUERIES: {QueryType.QUERY: academic_year_query, QueryType.MATCH_ID_QUERY: match_query},
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
                              'AY{current_year} Matched IDs Percent of AY{previous_year} Count'.format(current_year=current_year, previous_year=previous_year)]

        return statistics_headers

    def completion_headers(self):
        completion_headers = ['State', 'District', 'School', 'Grade', 'Category', 'Value', 'Assessment Subject',
                              'Assessment Type', 'Assessment Date', 'Academic Year', 'Count of Students Registered',
                              'Count of Students Assessed', 'Percent of Students Assessed']

        return completion_headers
