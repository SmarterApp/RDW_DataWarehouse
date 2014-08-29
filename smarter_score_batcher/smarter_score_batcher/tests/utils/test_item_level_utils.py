import unittest
from smarter_score_batcher.utils import item_level_utils
from pyramid import testing
from smarter_score_batcher.utils.meta import Meta

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class TestItemLevelUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        testing.tearDown()

    def test_get_all_item_level_for_tsb_csv(self):
        xml_string = '''<TestXML>
        <ElementOne key="">
        <ElementTwo context="FINAL" name="dummyValue" value="DummyState" />
        </ElementOne><Opportunity>
        <Item position="test" segmentId="segmentId_value"
        bankKey="test" key="key_value" operational="test" isSelected="test" format="test"
        score="test" scoreStatus="test" adminDate="test" numberVisits="test"
        mimeType="test" strand="test" contentLevel="test" pageNumber="test" pageVisits="test"
        pageTime="test" dropped="test">
        </Item>
        </Opportunity></TestXML>'''
        root = ET.fromstring(xml_string)
        meta = Meta(True, '213', None, None, None, None, None, None, None, None)
        row = item_level_utils.get_item_level_data(root, meta)
        self.assertEqual('key_value', row[0][0])
        self.assertEqual('segmentId_value', row[0][2])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
