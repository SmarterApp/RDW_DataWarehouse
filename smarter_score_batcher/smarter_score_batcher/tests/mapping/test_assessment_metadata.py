'''
Created on Aug 12, 2014

@author: dip
'''
import unittest
from smarter_score_batcher.mapping.assessment_metadata import JSONHeaders, JSONMapping,\
    get_assessment_metadata_mapping
from smarter_score_batcher.tests.mapping.utils import DummyObj, read_data
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class TestJSONMetadata(unittest.TestCase):

    def test_JSONHeaders_obj(self):
        out = JSONHeaders()
        values = out.get_values()
        self.assertIsNotNone(values)
        self.assertIsNone(values['Identification']['Guid'])
        out.asmt_guid = 'abc'
        self.assertEqual(values['Identification']['Guid'], 'abc')

    def test_JSONMapping(self):
        header = JSONHeaders()
        mapping = JSONMapping(DummyObj(), header, 'asmt_guid')
        mapping.evaluate()
        self.assertEqual(header.asmt_guid, 1)

    def test_get_json_mapping(self):
        data = read_data("assessment.xml")
        root = ET.fromstring(data)
        mapping = get_assessment_metadata_mapping(root)
        self.assertEqual(mapping['Identification']['Guid'], 'SBAC-FT-SomeDescription-MATH-7')
        self.assertEqual(mapping['Overall']['MinScore'], '1200')
        self.assertEqual(mapping['PerformanceLevels']['Level1']['Name'], 'Minimal Understanding')
        self.assertEqual(mapping['Claims']['Claim1']['MinScore'], '1200')
        self.assertEqual(mapping['Identification']['Subject'], 'MA')
        self.assertEqual(mapping['ClaimPerformanceLevels']['Level2']['Name'], 'At/Near Standard')

if __name__ == "__main__":
    unittest.main()
