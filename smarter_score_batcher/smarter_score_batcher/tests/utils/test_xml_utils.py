# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import unittest
from smarter_score_batcher.utils import xml_utils
from smarter_score_batcher.utils.constants import Constants
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

    def test_extract_meta_with_fallback_helper_final(self):
        xml_string = '''<TestXML>
        <ElementOne key="">
        <ElementTwo context="FINAL" name="dummyValue" value="DummyState" />
        </ElementOne>
        </TestXML>'''
        root = ET.fromstring(xml_string)
        state_name = xml_utils.extract_meta_with_fallback_helper(root, "./ElementOne/ElementTwo/[@name='dummyValue']", "value", "context")
        self.assertEqual('DummyState', state_name)

    def test_extract_meta_with_fallback_helper_initial(self):
        xml_string = '''<TestXML>
        <ElementOne key="">
        <ElementTwo context="INITIAL" name="dummyValue" value="DummyState" />
        </ElementOne>
        </TestXML>'''
        root = ET.fromstring(xml_string)
        state_name = xml_utils.extract_meta_with_fallback_helper(root, "./ElementOne/ElementTwo/[@name='dummyValue']", "value", "context")
        self.assertEqual('DummyState', state_name)

    def test_extract_meta_with_fallback_helper_no_value_attribute(self):
        xml_string = '''<TestXML>
        <ElementOne key="">
        <ElementTwo context="INITIAL" name="dummyValue" />
        </ElementOne>
        </TestXML>'''
        root = ET.fromstring(xml_string)
        state_name = xml_utils.extract_meta_with_fallback_helper(root, "./ElementOne/ElementTwo/[@name='dummyValue']", "value", "context")
        self.assertEqual(Constants.DEFAULT_VALUE, state_name)

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
