'''
Created on Aug 03, 2014

@author: sshrestha
'''
import unittest
import tempfile
import shutil
import os
from smarter_score_batcher import processors
from pyramid.registry import Registry
from pyramid import testing
from smarter_score_batcher.celery import setup_celery
from smarter_score_batcher.services import xml
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from smarter_score_batcher.tasks.remote_file_writer import remote_write
from unittest.mock import patch

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Test(unittest.TestCase):
    def setUp(self):
        self.tempfolder = tempfile.mkdtemp('tmp')
        # setup registry
        settings = {
            'smarter_score_batcher.celery_timeout': 30,
            'smarter_score_batcher.celery.celery_always_eager': True,
            'smarter_score_batcher.base_dir': self.tempfolder
        }
        reg = Registry()
        reg.settings = settings
        self.__config = testing.setUp(registry=reg)
        setup_celery(settings)

    def tearDown(self):
        shutil.rmtree(self.tempfolder)
        testing.tearDown()

    def test_process_xml_incomplete_xml(self):
        xml_string = '<xml></xml>'
        self.assertRaises(EdApiHTTPPreconditionFailed, processors.process_xml, xml_string)

    def test_process_xml_valid(self):
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
        result_process_xml = processors.process_xml(xml_string)
        meta_names = processors.extract_meta_names(xml_string)
        settings = self.__config.registry.settings
        file_path = processors.create_path(self.tempfolder, meta_names)
        args = (file_path, xml_string)
        queue_name = settings.get('smarter_score_batcher.sync_queue')
        celery_response = remote_write.apply_async(args=args, queue=queue_name)
        self.assertEqual(celery_response.get(timeout=settings.get('smarter_score_batcher.celery_timeout')), result_process_xml)

    def test_create_path_valid(self):
        meta = processors.Meta(True, 'student_id', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        path = os.path.join(self.tempfolder, 'student_id', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        create_path_result = processors.create_path(self.tempfolder, meta)
        self.assertEqual(path, create_path_result)

    def test_create_path_in_valid(self):
        meta = processors.Meta(True, 'NA', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        path = os.path.join(self.tempfolder, 'student_id', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        create_path_result = processors.create_path(self.tempfolder, meta)
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
