# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
