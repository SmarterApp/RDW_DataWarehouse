'''
Created on Aug 12, 2014

@author: tosako
'''
import unittest
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from smarter_score_batcher.utils.meta import extract_meta_names


class Test(unittest.TestCase):

    def test_extract_meta_names_empty_xml(self):
        xml_string = ''
        self.assertRaises(EdApiHTTPPreconditionFailed, extract_meta_names, xml_string)

    def test_extract_meta_names_incomplete_xml(self):
        xml_string = '<xml></xml>'
        meta = extract_meta_names(xml_string)
        self.assertFalse(meta.valid_meta)

    def test_extract_meta_names_valid_minimum_xml(self):
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="">
        <ExamineeAttribute context="FINAL" name="StudentIdentifier" value="CA-9999999598" />
        <ExamineeAttribute context="INITIAL" name="StudentIdentifier" value="CA-9999999598" />
        <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="FINAL" name="StateName" value="California" />
        <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="INITIAL" name="StateName" value="California" />
        </Examinee>
        </TDSReport>'''
        meta = extract_meta_names(xml_string)
        self.assertTrue(meta.valid_meta)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
