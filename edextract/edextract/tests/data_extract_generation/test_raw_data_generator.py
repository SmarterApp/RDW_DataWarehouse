__author__ = 'sravi'

"""Unit tests for raw data xml extract generator"""

import os
import shutil
import tempfile
import glob
import xml.etree.cElementTree as ET

from sqlalchemy.sql.expression import and_, select

from edcore.security.tenant import set_tenant_map
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edcore.tests.utils.unittest_with_edcore_sqlite import (get_unittest_tenant_name, Unittest_with_edcore_sqlite,
                                                            UnittestEdcoreDBConnection)
from edextract.data_extract_generation.raw_data_generator import generate_raw_data_xml
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, QueryType


class TestRawDataGenerator(Unittest_with_stats_sqlite, Unittest_with_edcore_sqlite):
    __tmp_raw_dir = tempfile.mkdtemp('raw_data_files')
    __built_files = False

    def setUp(self):
        self.__tmp_out_dir = tempfile.mkdtemp('raw_data_extract_output_dir')
        self._tenant = get_unittest_tenant_name()
        self.__state_code = 'NC'
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        if not TestRawDataGenerator.__built_files:
            self.__build_raw_data_files()
            TestRawDataGenerator.__built_files = True

    def tearDown(self):
        shutil.rmtree(self.__tmp_out_dir)

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TestRawDataGenerator.__tmp_raw_dir)
        Unittest_with_edcore_sqlite.tearDownClass()
        # Unittest_with_stats_sqlite.tearDownClass()  # Not sure why we don't need to do this

    def test_generate_raw_data_xml_files(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2015',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3'}
        query = self.__create_query(params)
        output_path = self.__tmp_out_dir
        task_info = {Constants.TASK_ID: '01',
                     Constants.CELERY_TASK_ID: '02',
                     Constants.REQUEST_GUID: '03'}
        extract_args = {TaskConstants.TASK_QUERIES: {QueryType.QUERY: query},
                        TaskConstants.ROOT_DIRECTORY: TestRawDataGenerator.__tmp_raw_dir}
        generate_raw_data_xml(self._tenant, output_path, task_info, extract_args)
        self.assertTrue(os.path.exists(output_path))
        extracted_files = glob.glob(os.path.join(output_path, "*.xml"))
        self.assertEqual(len(extracted_files), 42)
        for raw_xml_file in extracted_files:
            self.assertTrue(raw_xml_file.endswith('.xml'))

    def __create_query(self, params):
        with UnittestEdcoreDBConnection() as connection:
            dim_asmt = connection.get_table('dim_asmt')
            fact_asmt_outcome_vw = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact_asmt_outcome_vw.c.state_code,
                            fact_asmt_outcome_vw.c.asmt_year,
                            fact_asmt_outcome_vw.c.asmt_type,
                            dim_asmt.c.effective_date,
                            fact_asmt_outcome_vw.c.asmt_subject,
                            fact_asmt_outcome_vw.c.asmt_grade,
                            fact_asmt_outcome_vw.c.district_guid,
                            fact_asmt_outcome_vw.c.student_guid],
                           from_obj=[fact_asmt_outcome_vw
                                     .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id))])

            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_year == params['asmtYear']))
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_type == params['asmtType']))
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_subject == params['asmtSubject']))
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == params['asmtGrade']))
            query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == 'C'))
            return query

    def __get_path_to_raw_xml_for_student(self, root_dir, relative_file_path, record):
        return os.path.join(root_dir, relative_file_path, (str(record['student_guid']) + '.xml'))

    def __build_raw_data_files(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt = connection.get_table('fact_asmt_outcome_vw')
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
                raw_file_relative_path = os.path.join(str(result['state_code']).upper(),
                                        str(result['asmt_year']), str(result['asmt_type']).upper().replace(' ', '_'),
                                        str(result['effective_date']), str(result['asmt_subject']).upper(),
                                        str(result['asmt_grade']), str(result['district_guid']))

                raw_file_final_output_path = os.path.join(TestRawDataGenerator.__tmp_raw_dir, raw_file_relative_path)
                if not os.path.exists(raw_file_final_output_path):
                    os.makedirs(raw_file_final_output_path)

                path_to_xml_file= self.__get_path_to_raw_xml_for_student(TestRawDataGenerator.__tmp_raw_dir,
                                                                         raw_file_relative_path, result)
                root = ET.Element("root")
                student_node = ET.SubElement(root, "student")
                student_node.set("guid", str(result['student_guid']))
                tree = ET.ElementTree(root)
                tree.write(path_to_xml_file)
