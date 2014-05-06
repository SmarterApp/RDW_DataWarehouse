__author__ = 'nestep'

"""
Module containing assessment item-level generator unit tests.
"""

import tempfile
import shutil

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, get_unittest_tenant_name)
from edextract.data_extract_generation.item_level_generator import generate_items_csv, _get_path_to_item_csv


class TestItemLevelGenerator(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self._tenant = get_unittest_tenant_name()

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    def test_get_path_to_item_csv_summative(self):
        items_root_dir = '/opt/edware/item_level'
        record = {'code_state': 'NC', 'asmt_year': 2015, 'asmt_type': 'SUMMATIVE', 'effective_date': 20150402,
                  'asmt_subject': 'Math', 'grade_asmt': 3, 'guid_district': '3ab54de78a', 'guid_student': 'a78dbf34'}
        path = _get_path_to_item_csv(items_root_dir, record)
        self.assertEqual(path, '/opt/edware/item_level/NC/2015/SUMMATIVE/20150402/MATH/3/3ab54de78a/a78dbf34.csv')

    def test_get_path_to_item_csv_interim(self):
        items_root_dir = '/opt/edware/item_level'
        record = {'code_state': 'NC', 'asmt_year': 2015, 'asmt_type': 'INTERIM COMPREHENSIVE',
                  'effective_date': 20150106, 'asmt_subject': 'ELA', 'grade_asmt': 3, 'guid_district': '3ab54de78a',
                  'guid_student': 'a78dbf34'}
        path = _get_path_to_item_csv(items_root_dir, record)
        self.assertEqual(path,
                         '/opt/edware/item_level/NC/2015/INTERIM_COMPREHENSIVE/20150106/ELA/3/3ab54de78a/a78dbf34.csv')
