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
Created on Feb 25, 2013

@author: tosako
'''
import unittest
from edauth.saml2.saml_idp_metadata_manager import IDP_metadata_manager
from edauth.tests.test_helper.read_resource import read_resource
from edauth.saml2.saml_response_signature_verification import SAMLResposneSignatureVerification
import os


class Test(unittest.TestCase):

    def setUp(self):
        os.environ['PATH'] += os.pathsep + '/usr/local/bin'

    def test_verfication_without_metadata(self):
        manager = IDP_metadata_manager(None)
        pem_file = manager.get_trusted_pem_filename()
        verification = SAMLResposneSignatureVerification(pem_file, read_resource('SAMLResponse.txt'))
        self.assertFalse(verification.verify_signature())

    def test_verification_with_correct_metadata(self):
        manager = IDP_metadata_manager(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        pem_file = manager.get_trusted_pem_filename()
        verification = SAMLResposneSignatureVerification(pem_file, read_resource('SAMLResponse.txt'))
        self.assertTrue(verification.verify_signature())

    def test_verification_with_incorrect_response_format(self):
        manager = IDP_metadata_manager(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        pem_file = manager.get_trusted_pem_filename()
        verification = SAMLResposneSignatureVerification(pem_file, read_resource('SAMLResponse.xml'))
        self.assertFalse(verification.verify_signature())
# metadata = metadata = SAML_IDP_Metadata(create_xml_from_resources('IDP_Metadata.xml'))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
