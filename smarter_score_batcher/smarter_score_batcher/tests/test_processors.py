'''
Created on Aug 03, 2014

@author: sshrestha
'''
import unittest
import tempfile
import os
from smarter_score_batcher import processors
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from pyramid.registry import Registry
from pyramid import testing

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Test(unittest.TestCase):
    def setUp(self):
        settings = {
            'smarter_score_batcher.base_dir': '/tmp'
        }
        reg = Registry()
        reg.settings = settings
        self.__config = testing.setUp(registry=reg)

    def tearDown(self):
        testing.tearDown()
        
    def test_create_path_valid(self):
        meta = processors.Meta( True, 'student_id', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        self.assertEqual('/tmp/student_id/state_name/district_id/academic_year/asmt_type/subject/grade/effective_date', processors.create_path(self.__config.registry.settings.get('smarter_score_batcher.base_dir'), meta))
        
    def test_create_path_in_valid(self):
        meta = processors.Meta( True, 'NA', 'state_name', 'district_id', 'academic_year', 'asmt_type', 'subject', 'grade', 'effective_date')
        self.assertNotEqual('/tmp/student_id/state_name/district_id/academic_year/asmt_type/subject/grade/effective_date', processors.create_path(self.__config.registry.settings.get('smarter_score_batcher.base_dir'), meta))
        
        
    def test_extract_meta_names_empty_xml(self):
        xml_string = ''
        self.assertRaises(EdApiHTTPPreconditionFailed, processors.extract_meta_names, xml_string)
        
    def test_extract_meta_names_incomplete_xml(self):
        xml_string = '<xml></xml>'
        meta = processors.extract_meta_names(xml_string)
        self.assertFalse(meta.valid_meta)
        
    def test_extract_meta_names_valid_minimum_xml(self):
        xml_string = '<TDSReport>'
        xml_string= xml_string + ' <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />'
        xml_string= xml_string + ' <Examinee key="">'
        xml_string= xml_string + ' <ExamineeAttribute context="FINAL" name="SSID" value="CA-9999999598" />'
        xml_string= xml_string + ' <ExamineeAttribute context="INITIAL" name="SSID" value="CA-9999999598" />'
        xml_string= xml_string + ' <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />'
        xml_string= xml_string + ' <ExamineeRelationship context="FINAL" name="StateName" value="California" />'
        xml_string= xml_string + ' <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />'
        xml_string= xml_string + ' <ExamineeRelationship context="INITIAL" name="StateName" value="California" />'
        xml_string= xml_string + ' </Examinee>'
        xml_string= xml_string + ' </TDSReport>'
        meta = processors.extract_meta_names(xml_string)
        self.assertTrue(meta.valid_meta)
        
    def test_extract_meta_with_fallback_helper(self):
        xml_string = '<TestXML>'
        xml_string= xml_string + ' <ElementOne key="">'
        xml_string= xml_string + ' <ElementTwo context="FINAL" name="dummyValue" value="DummyState" />'
        xml_string= xml_string + ' </ElementOne>'
        xml_string= xml_string + ' </TestXML>'
        root = ET.fromstring(xml_string)
        state_name = processors.extract_meta_with_fallback_helper(root, "./ElementOne/ElementTwo/[@name='dummyValue']", "value", "context" )
        self.assertEqual('DummyState', state_name)
    
    def test_extract_meta_without_fallback_helper(self):
        xml_string = '<TestXML>'
        xml_string= xml_string + ' <ElementOne context="FINAL" name="StateName" dummyAttribute="DummyValue" />'
        xml_string= xml_string + ' </TestXML>'
        root = ET.fromstring(xml_string)
        state_name = processors.extract_meta_without_fallback_helper(root, "./ElementOne", "dummyAttribute" )
        self.assertEqual('DummyValue', state_name)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
