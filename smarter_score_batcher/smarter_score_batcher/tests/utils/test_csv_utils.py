import unittest
import tempfile
import os
import csv
from unittest.mock import patch
from smarter_score_batcher.utils.file_utils import file_writer, create_path
from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.celery import setup_celery
import uuid
from edcore.utils.file_utils import generate_path_to_raw_xml, \
    generate_path_to_item_csv
from smarter_score_batcher.utils.meta import Meta
from smarter_score_batcher.utils.file_lock import FileLock
from smarter_score_batcher.processing.file_processor import generate_csv_from_xml, \
    process_assessment_data
from smarter_score_batcher.error.exceptions import TSBException
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite
from smarter_score_batcher.database.db_utils import get_assessments, get_metadata, get_all_assessment_guids
from smarter_score_batcher.utils.constants import Constants


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from zope.component.globalregistry import base


class TestCSVUtils(Unittest_with_tsb_sqlite):
    def setUp(self):
        self.__tempfolder = tempfile.TemporaryDirectory()
        # setup registry
        settings = {
            'smarter_score_batcher.celery_timeout': 30,
            'smarter_score_batcher.celery.celery_always_eager': True,
            'smarter_score_batcher.base_dir': self.__tempfolder.name
        }
        reg = Registry()
        reg.utilities = base.utilities
        reg.settings = settings
        self.__config = testing.setUp(registry=reg)
        setup_celery(settings, db_connection=False)

    def tearDown(self):
        self.__tempfolder.cleanup()
        testing.tearDown()

    def test_generate_csv_from_xml(self):
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = '''<TDSReport>
        <Test subject="MATH" testId="SBAC-FT-SomeDescription-ELA-7" grade="3" assessmentType="Summative" academicYear="2014" />
        <Examinee key="12">
        <ExamineeRelationship context="INITIAL" name="StateAbbreviation" entityKey="3" value="CA"  contextDate="2014-04-14T11:13:41.803"/>
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
        generate_csv_from_xml(meta_names, csv_file_path, xml_file_path, work_dir, metadata_queue='test')
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
        self.assertRaises(TSBException, generate_csv_from_xml, meta_names, csv_file_path, xml_file_path, work_dir, metadata_queue='test')

    @patch('smarter_score_batcher.processing.file_processor.process_assessment_data')
    def test_generate_csv_from_xml_parse_exception(self, mock_process_assessment_data):
        mock_process_assessment_data.side_effect = Exception()
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = '''<TDSReport>
        <Test subject="MATH" grade="3" assessmentType="Summative" academicYear="2014" />
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
        self.assertRaises(TSBException, generate_csv_from_xml, meta_names, csv_file_path, xml_file_path, work_dir, metadata_queue='test')

    @patch('smarter_score_batcher.processing.file_processor.process_item_level_data')
    def test_generate_csv_from_xml_parse_exception_written(self, mock_process_item_level_data):
        mock_process_item_level_data.return_value = True
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        work_dir = os.path.join(self.__tempfolder.name, "work")
        xml_string = '''<TDSReport>
        <Test subject="MATH" grade="3" assessmentType="Summative" academicYear="2014" />
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
        self.assertRaises(TSBException, generate_csv_from_xml, meta_names, csv_file_path, xml_file_path, work_dir, metadata_queue='test')

    def test_process_assessment_data(self):
        base_dir = os.path.join(self.__tempfolder.name, 'work')
        xml_string = '''<TDSReport>
        <Test subject="MATH" grade="3" testId="SBAC-FT-SomeDescription-ELA-7" assessmentType="Summative" academicYear="2014" />
        <Examinee key="134">
        <ExamineeRelationship context="INITIAL" name="StateAbbreviation" entityKey="3" value="CA"  contextDate="2014-04-14T11:13:41.803"/>
        </Examinee>
        <Opportunity>
        </Opportunity>
        </TDSReport>'''
        meta = Meta(True, 'test1', 'state_code', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8', 'asmt_id')
        root = ET.fromstring(xml_string)
        process_assessment_data(root, meta)
        # test asmt guids
        asmt_guids = get_all_assessment_guids()
        self.assertIsNotNone(asmt_guids)
        state_code, asmt_guid = next(iter(asmt_guids))
        self.assertEqual(state_code, 'CA')
        self.assertEqual(asmt_guid, 'SBAC-FT-SomeDescription-ELA-7')
        # test metadata
        asmt_meta = get_metadata(asmt_guid)
        self.assertIsNotNone(asmt_meta)
        self.assertIsNotNone(asmt_meta[0][Constants.CONTENT])
        assessments = get_assessments(asmt_guid)
        self.assertIsNotNone(assessments)
        self.assertEqual(len(assessments), 3)
        guids, rows, headers = assessments
        self.assertEqual(len(guids), 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(headers), 88)

    def test_lock_and_write_IOError(self):
        temp_file = os.path.join(self.__tempfolder.name, str(uuid.uuid4()))
        fl = FileLock(temp_file)
        self.assertRaises(IOError, FileLock, temp_file, no_block_lock=True)


if __name__ == "__main__":
    unittest.main()
