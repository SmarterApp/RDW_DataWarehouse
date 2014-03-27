__author__ = 'tshewchuk'

"""
Module containing Student Registration report generator unit tests.
"""

import os
import tempfile
import shutil
import csv
import json
from sqlalchemy.sql.expression import select

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (Unittest_with_edcore_sqlite, UnittestEdcoreDBConnection,
                                                            get_unittest_tenant_name)
from edextract.data_extract_generation.query_extract_generator import generate_csv, generate_json, _generate_csv_data
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from unittest.mock import MagicMock


class TestQueryExtractGenerator(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self._tenant = get_unittest_tenant_name()

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)

    def test_generate_csv_success(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid, dim_asmt.c.asmt_period], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '22')
        output = os.path.join(self.__tmp_dir, 'asmt.csv')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.TASK_QUERY: query}
        generate_csv(self._tenant, output, task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 2)
        self.assertEqual(csv_data[0], ['asmt_guid', 'asmt_period'])
        self.assertEqual(csv_data[1], ['22', 'Spring 2016'])

    def test_generate_json_success(self):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            query = select([dim_asmt.c.asmt_guid], from_obj=[dim_asmt])
            query = query.where(dim_asmt.c.asmt_guid == '22')
            output = os.path.join(self.__tmp_dir, 'asmt.json')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.TASK_QUERY: query}
        generate_json(self._tenant, output, task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        with open(output) as out:
            data = json.load(out)
        self.assertEqual(data['asmt_guid'], '22')

    def test_generate_csv_data_no_result(self):
        #Results are empty
        results = self.dummy_empty_iterator()

        header, data = _generate_csv_data(results)
        self.assertEqual(len(header), 0)
        self.assertEqual(len(data), 0)

    def dummy_empty_iterator(self):
        for ctr in range(0, 0):
            yield ctr
