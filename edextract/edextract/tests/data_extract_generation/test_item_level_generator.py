__author__ = 'nestep'

"""
Module containing assessment item-level generator unit tests.
"""

import csv
import os
import shutil
import tempfile

from sqlalchemy.sql.expression import and_, select

from edcore.security.tenant import set_tenant_map
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (get_unittest_tenant_name, Unittest_with_edcore_sqlite,
                                                            UnittestEdcoreDBConnection)
from edextract.data_extract_generation.item_level_generator import generate_items_csv, _get_path_to_item_csv
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from smarter.extracts.student_assessment import get_extract_assessment_item_query


class TestItemLevelGenerator(Unittest_with_stats_sqlite, Unittest_with_edcore_sqlite):

    def setUp(self):
        self.__tmp_out_dir = tempfile.mkdtemp('item_file_archiver_test')
        #self.__tmp_item_dir = '/opt/edware/item_level_ut'
        self.__tmp_item_dir = tempfile.mkdtemp('item_level_files')
        self._tenant = get_unittest_tenant_name()
        self.__state_code = 'NC'
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        self.__build_item_level_files()

    def tearDown(self):
        shutil.rmtree(self.__tmp_out_dir)
        #shutil.rmtree(self.__tmp_item_dir)

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def test_generate_item_csv_success_no_item_ids(self):
        #3181376a-f3a8-40d3-bbde-e65fdd9f4494
        params = {'stateCode': 'NC',
                  'asmtYear': '2015',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3'}
        #query = get_extract_assessment_item_query(params)
        query = None
        output = os.path.join(self.__tmp_out_dir, 'items.csv')
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.TASK_QUERIES: {QueryType.QUERY: query},
                        TaskConstants.ROOT_DIRECTORY: self.__tmp_item_dir,
                        TaskConstants.ITEM_IDS: None}
        generate_items_csv(self._tenant, output, task_info, extract_args)
        self.assertTrue(os.path.exists(output))
        csv_data = []
        with open(output) as out:
            data = csv.reader(out)
            for row in data:
                csv_data.append(row)
        self.assertEqual(len(csv_data), 2)
        self.assertEqual(csv_data[0], ['asmt_guid', 'asmt_period'])
        self.assertEqual(csv_data[1], ['7d10d26b-b013-4cdd-a916-5d577e895cff', 'Spring 2016'])

    def test_get_path_to_item_csv_summative(self):
        print(self.__state_code)
        items_root_dir = '/opt/edware/item_level'
        record = {'state_code': 'NC',
                  'asmt_year': 2015,
                  'asmt_type': 'SUMMATIVE',
                  'effective_date': 20150402,
                  'asmt_subject': 'Math',
                  'asmt_grade': 3,
                  'district_guid': '3ab54de78a',
                  'student_guid': 'a78dbf34'}
        path = _get_path_to_item_csv(items_root_dir, record)
        self.assertEqual(path, '/opt/edware/item_level/NC/2015/SUMMATIVE/20150402/MATH/3/3ab54de78a/a78dbf34.csv')

    def test_get_path_to_item_csv_interim(self):
        items_root_dir = '/opt/edware/item_level'
        record = {'state_code': 'NC',
                  'asmt_year': 2015,
                  'asmt_type': 'INTERIM COMPREHENSIVE',
                  'effective_date': 20150106,
                  'asmt_subject': 'ELA',
                  'asmt_grade': 3,
                  'district_guid': '3ab54de78a',
                  'student_guid': 'a78dbf34'}
        path = _get_path_to_item_csv(items_root_dir, record)
        self.assertEqual(path,
                         '/opt/edware/item_level/NC/2015/INTERIM_COMPREHENSIVE/20150106/ELA/3/3ab54de78a/a78dbf34.csv')

    def __build_item_pool(self, asmt_count):
        pool = []
        for i in range(10):
            pool.append({'key': i + (asmt_count * 10), 'client': i + (asmt_count * 10),
                         'type': 'MC', 'segment': 'segment_name_ut'})
        return pool

    def __build_item_level_files(self):
        a = 0
        with UnittestEdcoreDBConnection() as connection:
            item_pools, asmt_count, flip_flop = {}, 0, False
            fact_asmt = connection.get_table('fact_asmt_outcome')
            dim_asmt = connection.get_table('dim_asmt')
            query = select([fact_asmt.c.state_code, fact_asmt.c.asmt_year, fact_asmt.c.asmt_type,
                            dim_asmt.c.effective_date, fact_asmt.c.asmt_subject, fact_asmt.c.asmt_grade,
                            fact_asmt.c.district_guid, fact_asmt.c.student_guid, fact_asmt.c.asmt_guid],
                           from_obj=[fact_asmt
                                     .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt.c.asmt_rec_id))])
            query = query.where(fact_asmt.c.rec_status == 'C')
            query = query.order_by(fact_asmt.c.asmt_guid, fact_asmt.c.student_guid)
            results = connection.get_result(query)
            for result in results:
                asmt_guid = result['asmt_guid']
                if asmt_guid not in item_pools:
                    item_pools[asmt_guid] = self.__build_item_pool(asmt_count)
                    asmt_count += 1
                    flip_flop = False

                if flip_flop:
                    student_pool = item_pools[asmt_guid][0:5]
                else:
                    student_pool = item_pools[asmt_guid][5:10]
                flip_flop = not flip_flop

                dir_path = os.path.join(self.__tmp_item_dir, str(result['state_code']).upper(), str(result['asmt_year']),
                                        str(result['asmt_type']).upper().replace(' ', '_'),
                                        str(result['effective_date']), str(result['asmt_subject']).upper(),
                                        str(result['asmt_grade']), str(result['district_guid']))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                with open(_get_path_to_item_csv(self.__tmp_item_dir, result), 'w') as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    for item in student_pool:
                        csv_writer.writerow([item['key'], result['student_guid'], item['segment'], 0, item['client'],
                                             1, 1, item['type'], 0, 1, '2013-04-03T16:21:33.660', 1, 'MA-Undesignated',
                                             'MA-Undesignated', 1, 1, 1, 0])
                    csv_writer.writerow([asmt_guid])
