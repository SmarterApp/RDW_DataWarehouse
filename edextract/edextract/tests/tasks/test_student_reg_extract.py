__author__ = 'tshewchuk'

"""
This module contains methods to test the Student Registration extraction logic.
"""

import unittest
import tempfile
import os
import shutil
import csv

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, UnittestEdcoreDBConnection,
                                                            get_unittest_tenant_name)
from edextract.tasks.extract import generate_extract_file
from edextract.data_extract_generation.student_reg_report_generator import generate_statistics_report, generate_completion_report

from edextract.celery import setup_celery
from edextract.tasks.student_reg_constants import Constants
from edextract.exceptions import ExtractionError
from edextract.settings.config import setup_settings


class TestStudentRegExtractTask(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        here = os.path.abspath(os.path.dirname(__file__))
        gpg_home = os.path.abspath(os.path.join(here, "..", "..", "..", "..", "config", "gpg"))
        settings = {'extract.celery.BROKER_URL': 'memory',
                    'extract.gpg.keyserver': None,
                    'extract.gpg.homedir': gpg_home,
                    'extract.gpg.public_key.cat': 'kswimberly@amplify.com',
                    'extract.celery.CELERY_ALWAYS_EAGER': 'True',
                    'extract.retries_allowed': '1',
                    'extract.retry_delay': '60'
                    }
        setup_celery(settings)
        setup_settings(settings)
        self._tenant = get_unittest_tenant_name()
        self.__files = ['a.txt', 'b.txt', 'c.txt']
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        for file in self.__files:
            with open(os.path.join(self.__tmp_dir, file), "w") as f:
                f.write('hello ' + file)

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    def test_generate_statistics_csv_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        extract_args = {Constants.ACADEMIC_YEAR: 2014}
        result = generate_extract_file.apply(args=[self._tenant, '0', '1', output, generate_statistics_report, extract_args])
        result.get()
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

    def test_generate_completion_csv_success(self):
        output = os.path.join(self.__tmp_dir, 'stureg_comp.csv')
        extract_args = {Constants.ACADEMIC_YEAR: 2014}
        result = generate_extract_file.apply(args=[self._tenant, '0', '1', output, generate_completion_report, extract_args])
        result.get()
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

    def test_generate_csv_no_tenant(self):
        output = os.path.join(self.__tmp_dir, 'stureg_stat.csv')
        extract_args = {Constants.ACADEMIC_YEAR: 2014}
        result = generate_extract_file.apply(args=[None, '0', '1', output, generate_statistics_report, extract_args])
        result.get()
        self.assertFalse(os.path.exists(output))

    def test_generate_csv_bad_file(self):
        output = 'C:'
        extract_args = {Constants.ACADEMIC_YEAR: 2014}
        result = generate_extract_file.apply(args=[self._tenant, '0', '1', output, generate_statistics_report, extract_args])
        self.assertRaises(ExtractionError, result.get,)


if __name__ == "__main__":
    unittest.main()
