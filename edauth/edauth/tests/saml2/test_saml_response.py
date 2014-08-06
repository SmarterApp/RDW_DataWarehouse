'''
Created on Feb 16, 2013

@author: tosako
'''
import unittest
from edauth.tests.test_helper.read_resource import create_SAMLResponse


class Test(unittest.TestCase):

    def test_attributes(self):
        samlResponse = create_SAMLResponse('SAMLResponse.xml')
        assertions = samlResponse.get_assertion()
        self.assertIsNotNone(assertions, 'SAML Response has assetions')

        attributes = assertions.get_attributes()
        self.assertIsNotNone(attributes, 'assertions have attributes')
        self.assertEqual(5, len(attributes), 'attributes does not have 5 items')

    def test_id(self):
        samlResponse = create_SAMLResponse('SAMLResponse.xml')
        self.assertEqual('s2c39419140bad5e9c015019bcaa49215bf00d0322', samlResponse.get_id(), 'read ID correctly')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
