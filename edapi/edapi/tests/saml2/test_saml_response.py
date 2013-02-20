'''
Created on Feb 16, 2013

@author: tosako
'''
import unittest
import os
from xml.dom.minidom import parseString
from edapi.saml2.saml_response import SAMLResponse


class Test(unittest.TestCase):

    def test_attributes(self):
        samlResponse = create_SAMLResponse()
        assertions = samlResponse.get_assertion()
        self.assertIsNotNone(assertions, 'SAML Response has assetions')

        attributes = assertions.get_attributes()
        self.assertIsNotNone(attributes, 'assertions have attributes')
        self.assertEqual(3, len(attributes), 'attributes are array and has 3 items')

    def test_id(self):
        samlResponse = create_SAMLResponse()
        self.assertEqual('s2c39419140bad5e9c015019bcaa49215bf00d0322', samlResponse.get_id(), 'read ID correctly')


def create_SAMLResponse():
    saml_xml = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'SAMLResponse.xml'))
    with open(saml_xml, 'r') as f:
        xml = f.read()
    f.close()
    __dom_SAMLResponse = parseString(xml)
    samlResponse = SAMLResponse(__dom_SAMLResponse)
    return samlResponse

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
