import unittest
from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest
from smarter_score_batcher.celery import setup_celery
from unittest.mock import patch
import os
from smarter_score_batcher.services.xml import xml_catcher, pre_process_xml,\
    post_process_xml
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
import uuid
import hashlib
import tempfile
from smarter_score_batcher.utils.meta import extract_meta_names
from smarter_score_batcher.utils.file_utils import create_path, file_writer
from edcore.utils.file_utils import generate_path_to_raw_xml,\
    generate_path_to_item_csv
from smarter_score_batcher.utils import meta
import csv
here = os.path.abspath(os.path.dirname(__file__))
xsd_file_path = os.path.abspath(os.path.join(here, '..', '..', '..', 'resources', 'sample_xsd.xsd'))


class TestXML(unittest.TestCase):

    def setUp(self):
        self.__tempfolder = tempfile.TemporaryDirectory()
        # setup request
        self.__request = DummyRequest()
        self.__request.method = 'POST'
        # setup registry
        settings = {
            'smarter_score_batcher.celery_timeout': 30,
            'smarter_score_batcher.celery.celery_always_eager': True,
            'smarter_score_batcher.base_dir': self.__tempfolder.name
        }
        reg = Registry()
        reg.settings = settings
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        setup_celery(settings)

    def tearDown(self):
        testing.tearDown()

    @patch('smarter_score_batcher.services.xml.extract_meta_names')
    @patch('smarter_score_batcher.services.xml.post_process_xml')
    @patch('smarter_score_batcher.services.xml.pre_process_xml')
    def test_xml_catcher_succeed(self, mock_process_xml, mock_create_item_level_csv, mock_extract_meta_names):
        mock_process_xml.return_value = True
        mock_extract_meta_names.return_value.valid_meta.return_value = True
        self.__request.body = '<xml></xml>'
        response = xml_catcher(self.__request)
        self.assertEqual(response.status_code, 200, "should return 200 after writing xml file")

    @patch('smarter_score_batcher.services.xml.pre_process_xml')
    def test_xml_catcher_failed(self, mock_process_xml):
        mock_process_xml.return_value = False
        self.__request.body = '<xml></xml>'
        self.assertRaises(EdApiHTTPPreconditionFailed, xml_catcher, self.__request)

    @patch('smarter_score_batcher.services.xml.pre_process_xml')
    def test_xml_catcher_no_content(self, mock_process_xml):
        mock_process_xml.side_effect = Exception()
        self.__request.body = ''
        self.assertRaises(Exception, xml_catcher, self.__request)

    @patch('smarter_score_batcher.services.xml.create_path')
    def test_process_xml_valid(self, mock_create_path):
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="12">
        <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="FINAL" name="StateName" value="California" />
        <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="INITIAL" name="StateName" value="California" />
        </Examinee>
        </TDSReport>'''
        m1 = hashlib.md5()
        m1.update(bytes(xml_string, 'utf-8'))
        digest1 = m1.digest()
        meta_names = extract_meta_names(xml_string)
        with tempfile.TemporaryDirectory() as tempfolder:
            target = os.path.join(tempfolder, str(uuid.uuid4()), str(uuid.uuid4()))
            mock_create_path.return_value = target

            result_process_xml = pre_process_xml(meta_names, xml_string, None, None, 0)
            self.assertTrue(result_process_xml)
            m2 = hashlib.md5()
            with open(target, 'rb') as f:
                m2.update(f.read())
            digest2 = m2.digest()
        self.assertEqual(digest1, digest2)

    def test_create_item_level_csv(self):
        root_dir_xml = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        root_dir_csv = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="12">
        <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="FINAL" name="StateName" value="California" />
        <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="INITIAL" name="StateName" value="California" />
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
        meta_names = meta.Meta(True, 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8')
        xml_file_path = create_path(root_dir_xml, meta_names, generate_path_to_raw_xml)
        file_writer(xml_file_path, xml_string)
        post_process_xml(root_dir_xml, root_dir_csv, None, meta_names)
        rows = []
        csv_file_path = create_path(root_dir_csv, meta_names, generate_path_to_item_csv)
        with open(csv_file_path, newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                rows.append(row)
        csv_first_row_list = ['key_value', '12', 'segmentId_value', 'position_value', '', 'operational_value', 'isSelected_value', 'format_type_value', 'score_value', 'scoreStatus_value', 'adminDate_value', 'numberVisits_value', 'strand_value', 'contentLevel_value', 'pageNumber_value', 'pageVisits_value', 'pageTime_value', 'dropped_value']
        self.assertEqual(1, len(rows))
        self.assertEqual(csv_first_row_list, rows[0])

if __name__ == '__main__':
    unittest.main()
