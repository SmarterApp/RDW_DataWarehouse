import unittest
import tempfile
import os
import csv
from unittest.mock import patch, PropertyMock
from smarter_score_batcher.utils.file_utils import file_writer, create_path
from smarter_score_batcher.utils import csv_utils
from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.celery import setup_celery
import uuid
from edcore.utils.file_utils import generate_path_to_raw_xml, \
    generate_path_to_item_csv
from smarter_score_batcher.utils.csv_utils import process_assessment_data, \
    generate_assessment_file, lock_and_write
from smarter_score_batcher.utils.meta import Meta
from smarter_score_batcher.utils.file_lock import FileLock
from smarter_score_batcher.mapping.assessment import get_assessment_mapping
import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class TestCSVUtils(unittest.TestCase):
    def setUp(self):
        self.__tempfolder = tempfile.TemporaryDirectory()
        # setup registry
        settings = {
            'smarter_score_batcher.celery_timeout': 30,
            'smarter_score_batcher.celery.celery_always_eager': True,
            'smarter_score_batcher.base_dir': self.__tempfolder.name
        }
        reg = Registry()
        reg.settings = settings
        self.__config = testing.setUp(registry=reg)
        setup_celery(settings)

    def tearDown(self):
        self.__tempfolder.cleanup()
        testing.tearDown()

    def test_generate_csv_from_xml(self):
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="12">
        </Examinee>
        <Opportunity>
        <Item position="position_value" segmentId="segmentId_value"
        bankKey="test" key="key_value" operational="operational_value" isSelected="isSelected_value" format="format_type_value"
        score="score_value" scoreStatus="scoreStatus_value" adminDate="adminDate_value" numberVisits="numberVisits_value"
        mimeType="test" strand="strand_value" contentLevel="contentLevel_value" pageNumber="pageNumber_value" pageVisits="pageVisits_value"
        pageTime="pageTime_value" dropped="dropped_value">
        </Item>
        </Opportunity>
        </TDSReport>'''
        meta_names = Meta(True, 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9')
        xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
        file_writer(xml_file_path, xml_string)
        rows = []
        csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
        csv_utils.generate_csv_from_xml(meta_names, csv_file_path, xml_file_path, work_dir)
        with open(csv_file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                rows.append(row)
        csv_first_row_list = ['key_value', 'test1', 'segmentId_value', 'position_value', '', 'operational_value', 'isSelected_value', 'format_type_value', 'score_value', 'scoreStatus_value', 'adminDate_value', 'numberVisits_value', 'strand_value', 'contentLevel_value', 'pageNumber_value', 'pageVisits_value', 'pageTime_value', 'dropped_value']
        self.assertEqual(1, len(rows))
        self.assertEqual(csv_first_row_list, rows[0])

    def test_generate_csv_from_xml_parse_error(self):
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = "bad xml"
        meta_names = Meta(True, 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9')
        xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
        file_writer(xml_file_path, xml_string)
        csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
        csv_utils.generate_csv_from_xml(meta_names, csv_file_path, xml_file_path, work_dir)
        self.assertRaises(ET.ParseError)

    @patch('smarter_score_batcher.utils.csv_utils.process_assessment_data')
    def test_generate_csv_from_xml_parse_exception(self, mock_process_assessment_data):
        mock_process_assessment_data.side_effect = Exception()
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="12">
        <Opportunity>
        <Item position="position_value" segmentId="segmentId_value"
        bankKey="test" key="key_value" operational="operational_value" isSelected="isSelected_value" format="format_type_value"
        score="score_value" scoreStatus="scoreStatus_value" adminDate="adminDate_value" numberVisits="numberVisits_value"
        mimeType="test" strand="strand_value" contentLevel="contentLevel_value" pageNumber="pageNumber_value" pageVisits="pageVisits_value"
        pageTime="pageTime_value" dropped="dropped_value">
        </Item>
        </Opportunity>
        </TDSReport>'''
        meta_names = Meta(True, 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9')
        xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
        file_writer(xml_file_path, xml_string)
        csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
        csv_utils.generate_csv_from_xml(meta_names, csv_file_path, xml_file_path, work_dir)
        self.assertFalse(os.path.isfile(csv_file_path))

    @patch('smarter_score_batcher.utils.csv_utils.metadata_generator_bottom_up')
    @patch('smarter_score_batcher.utils.csv_utils.process_item_level_data')
    def test_generate_csv_from_xml_parse_exception_written(self, mock_process_item_level_data, mock_metadata_generator_bottom_up):
        mock_process_item_level_data.return_value = True
        mock_metadata_generator_bottom_up.side_effect = Exception()
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="12">
        <Opportunity>
        <Item position="position_value" segmentId="segmentId_value"
        bankKey="test" key="key_value" operational="operational_value" isSelected="isSelected_value" format="format_type_value"
        score="score_value" scoreStatus="scoreStatus_value" adminDate="adminDate_value" numberVisits="numberVisits_value"
        mimeType="test" strand="strand_value" contentLevel="contentLevel_value" pageNumber="pageNumber_value" pageVisits="pageVisits_value"
        pageTime="pageTime_value" dropped="dropped_value">
        </Item>
        </Opportunity>
        </TDSReport>'''
        meta_names = Meta(True, 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'test9')
        xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
        file_writer(xml_file_path, xml_string)
        csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
        csv_utils.generate_csv_from_xml(meta_names, csv_file_path, xml_file_path, work_dir)
        self.assertFalse(os.path.isfile(csv_file_path))

    def test_process_assessment_data(self):
        base_dir = os.path.join(self.__tempfolder.name, 'work')
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="134"/>
        <Opportunity>
        </Opportunity>
        </TDSReport>'''
        meta = Meta(True, 'test1', 'state_code', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'asmt_id')
        root = ET.fromstring(xml_string)
        process_assessment_data(root, meta, base_dir)
        self.assertTrue(os.path.isfile(os.path.join(base_dir, 'state_code', 'asmt_id', 'asmt_id.csv')))
        self.assertTrue(os.path.isfile(os.path.join(base_dir, 'state_code', 'asmt_id', 'asmt_id.json')))

    def test_generate_assessment_file_when_file_exists(self):
        file_path = os.path.join(self.__tempfolder.name, 'testassessment.csv')
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3" assessmentType="Formative" academicYear="2014" />
        <Examinee key="134"/>
        <Opportunity>
        </Opportunity>
        </TDSReport>'''
        root = ET.fromstring(xml_string)
        # Tes tht athe file has 3 lines (1 header + 2 data)
        with open(file_path, 'a') as f:
            generate_assessment_file(f, root, header=True)
        self.assertTrue(os.path.isfile(file_path))
        rows = []
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                rows.append(row)
        self.assertTrue(len(rows), 2)
        with open(file_path, 'a') as f:
            generate_assessment_file(f, root, header=True)
        rows = []
        with open(file_path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                rows.append(row)
        self.assertTrue(len(rows), 3)

    @PropertyMock('smarter_score_batcher.utils.csv_utils.SPIN_LOCK')
    def test_lock_and_write_spin_lock(self, mock_SPIN_LOCK):
        file_path = os.path.join(self.__tempfolder.name, 'testassessment')
        fl = FileLock(file_path + '.csv')
        mock_SPIN_LOCK.return_value = [True, True, False]
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3" assessmentType="Formative" academicYear="2014" />
        <Examinee key="134"/>
        <Opportunity>
        </Opportunity>
        </TDSReport>'''
        root = ET.fromstring(xml_string)
        lock_and_write(root, file_path)
        self.assertEqual(3, mock_SPIN_LOCK.call_count)

    @patch('smarter_score_batcher.utils.csv_utils.lock_and_write')
    def test_generate_assessment_exception(self, mock_lock_and_write):
        mock_lock_and_write.side_effect = [Exception()]
        file_path = os.path.join(self.__tempfolder.name, 'testassessment.csv')
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3" assessmentType="Formative" academicYear="2014" />
        <Examinee key="134"/>
        <Opportunity>
        </Opportunity>
        </TDSReport>'''
        root = ET.fromstring(xml_string)
        self.assertRaises(Exception, generate_assessment_file, root, file_path)

    def test_lock_and_write_IOError(self):
        temp_file = os.path.join(self.__tempfolder.name, str(uuid.uuid4()))
        fl = FileLock(temp_file)
        self.assertRaises(IOError, FileLock, temp_file, no_block_lock=True)

if __name__ == "__main__":
    unittest.main()
