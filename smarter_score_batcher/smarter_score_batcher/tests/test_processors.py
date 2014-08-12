'''
Created on Aug 03, 2014

@author: sshrestha
'''
import unittest
import tempfile
import os
from smarter_score_batcher import processors
from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.celery import setup_celery
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from unittest.mock import patch
from edcore.utils.file_utils import generate_path_to_raw_xml
import hashlib
import uuid

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Test(unittest.TestCase):
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

    def test_process_xml_incomplete_xml(self):
        xml_string = '<xml></xml>'
        self.assertRaises(EdApiHTTPPreconditionFailed, processors.process_xml, xml_string)

    @patch('smarter_score_batcher.processors.create_path')
    def test_process_xml_valid(self, mock_create_path):
        target = os.path.join(self.__tempfolder.name, str(uuid.uuid4()), str(uuid.uuid4()))
        mock_create_path.return_value = target
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="">
        <ExamineeAttribute context="FINAL" name="SSID" value="CA-9999999598" />
        <ExamineeAttribute context="INITIAL" name="SSID" value="CA-9999999598" />
        <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="FINAL" name="StateName" value="California" />
        <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="INITIAL" name="StateName" value="California" />
        </Examinee>
        </TDSReport>'''
        result_process_xml = processors.process_xml(xml_string)
        self.assertTrue(result_process_xml)
        m1 = hashlib.md5()
        m1.update(bytes(xml_string, 'utf-8'))
        digest1 = m1.digest()
        m2 = hashlib.md5()
        with open(target, 'rb') as f:
            m2.update(f.read())
        digest2 = m2.digest()
        self.assertEqual(digest1, digest2)

    def test_create_path_valid(self):
        meta = processors.Meta(True, 'student_id', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        path = os.path.join(self.__tempfolder.name, 'state_name', 'academic_year', 'ASMT_TYPE', 'effective_date', 'SUBJECT', 'grade', 'district_id', 'student_id.xml')
        create_path_result = processors.create_path(self.__tempfolder.name, meta, generate_path_to_raw_xml)
        self.assertEqual(path, create_path_result)

    def test_create_path_invalid(self):
        meta = processors.Meta(True, 'NA', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        path = os.path.join(self.__tempfolder.name, 'student_id', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        create_path_result = processors.create_path(self.__tempfolder.name, meta, generate_path_to_raw_xml)
        self.assertNotEqual(path, create_path_result)

    def test_extract_meta_names_empty_xml(self):
        xml_string = ''
        self.assertRaises(EdApiHTTPPreconditionFailed, processors.extract_meta_names, xml_string)

    def test_extract_meta_names_incomplete_xml(self):
        xml_string = '<xml></xml>'
        meta = processors.extract_meta_names(xml_string)
        self.assertFalse(meta.valid_meta)

    def test_extract_meta_names_valid_minimum_xml(self):
        xml_string = '<TDSReport>'
        xml_string = xml_string + ' <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />'
        xml_string = xml_string + ' <Examinee key="">'
        xml_string = xml_string + ' <ExamineeAttribute context="FINAL" name="SSID" value="CA-9999999598" />'
        xml_string = xml_string + ' <ExamineeAttribute context="INITIAL" name="SSID" value="CA-9999999598" />'
        xml_string = xml_string + ' <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />'
        xml_string = xml_string + ' <ExamineeRelationship context="FINAL" name="StateName" value="California" />'
        xml_string = xml_string + ' <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />'
        xml_string = xml_string + ' <ExamineeRelationship context="INITIAL" name="StateName" value="California" />'
        xml_string = xml_string + ' </Examinee>'
        xml_string = xml_string + ' </TDSReport>'
        meta = processors.extract_meta_names(xml_string)
        self.assertTrue(meta.valid_meta)

    def test_extract_meta_with_fallback_helper(self):
        xml_string = '<TestXML>'
        xml_string = xml_string + ' <ElementOne key="">'
        xml_string = xml_string + ' <ElementTwo context="FINAL" name="dummyValue" value="DummyState" />'
        xml_string = xml_string + ' </ElementOne>'
        xml_string = xml_string + ' </TestXML>'
        root = ET.fromstring(xml_string)
        state_name = processors.extract_meta_with_fallback_helper(root, "./ElementOne/ElementTwo/[@name='dummyValue']", "value", "context")
        self.assertEqual('DummyState', state_name)

    def test_extract_meta_without_fallback_helper(self):
        xml_string = '<TestXML>'
        xml_string = xml_string + ' <ElementOne context="FINAL" name="StateName" dummyAttribute="DummyValue" />'
        xml_string = xml_string + ' </TestXML>'
        root = ET.fromstring(xml_string)
        state_name = processors.extract_meta_without_fallback_helper(root, "./ElementOne", "dummyAttribute")
        self.assertEqual('DummyValue', state_name)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
