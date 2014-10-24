'''
Created on Aug 12, 2014

@author: tosako
'''
import unittest
from edapi.httpexceptions import EdApiHTTPPreconditionFailed
from smarter_score_batcher.utils.meta import extract_meta_names
from smarter_score_batcher.error.exceptions import TSBException


class Test(unittest.TestCase):

    def test_extract_meta_names_empty_xml(self):
        xml_string = ''
        self.assertRaises(EdApiHTTPPreconditionFailed, extract_meta_names, xml_string)

    def test_extract_meta_names_incomplete_xml(self):
        xml_string = '<xml></xml>'
        self.assertRaises(TSBException, extract_meta_names, xml_string)

    def test_extract_meta_names_valid_minimum_xml(self):
        xml_string = '''<TDSReport>
        <Test subject="MA" grade="3-12" assessmentType="Formative" academicYear="2014" />
        <Examinee key="CA-9999999598">
        <ExamineeRelationship context="FINAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="FINAL" name="StateName" value="California" />
        <ExamineeRelationship context="INITIAL" name="DistrictID" value="CA_9999827" />
        <ExamineeRelationship context="INITIAL" name="StateAbbreviation" value="California" />
        </Examinee>
        <Opportunity effectiveDate="2014-02-02" />
        </TDSReport>'''
        meta = extract_meta_names(xml_string)
        self.assertTrue(meta.valid_meta)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
