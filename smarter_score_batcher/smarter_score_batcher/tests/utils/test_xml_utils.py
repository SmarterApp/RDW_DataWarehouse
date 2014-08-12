import unittest
from smarter_score_batcher.utils import xml_utils
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

    def test_extract_meta_with_fallback_helper(self):
        xml_string = '''<TestXML>
        <ElementOne key="">
        <ElementTwo context="FINAL" name="dummyValue" value="DummyState" />
        </ElementOne>
        </TestXML>'''
        root = ET.fromstring(xml_string)
        state_name = xml_utils.extract_meta_with_fallback_helper(root, "./ElementOne/ElementTwo/[@name='dummyValue']", "value", "context")
        self.assertEqual('DummyState', state_name)

    def test_extract_meta_without_fallback_helper(self):
        xml_string = '''<TestXML>
        <ElementOne context="FINAL" name="StateName" dummyAttribute="DummyValue" />
        </TestXML>'''
        root = ET.fromstring(xml_string)
        state_name = xml_utils.extract_meta_without_fallback_helper(root, "./ElementOne", "dummyAttribute")
        self.assertEqual('DummyValue', state_name)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
