import unittest
from smarter_score_batcher.utils import csv_utils
from pyramid import testing

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        testing.tearDown()

    def test_get_all_elements(self):
        xml_string = '''<TestXML>
        <ElementOne key="">
        <ElementTwo context="FINAL" name="dummyValue" value="DummyState" />
        </ElementOne>
        </TestXML>'''
        root = ET.fromstring(xml_string)
        attributeDict = csv_utils.get_all_elements(root, "./ElementOne/ElementTwo")
        self.assertTrue('name' in attributeDict)

    def test_get_all_elements_for_tsb_csv(self):
        csv_utils.get_all_elements_for_tsb_csv(root, element_to_get)
        
        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
