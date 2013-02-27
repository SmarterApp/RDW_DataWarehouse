'''
Created on Feb 25, 2013

@author: tosako
'''
import unittest
from edauth.saml2.saml_idp_metadata_manager import IDP_metadata_manger
from edauth.tests.test_helper.read_resource import read_resource
from edauth.saml2.saml_response_signature_verification import SAMLResposneSignatureVerification
import os


class Test(unittest.TestCase):

    def setUp(self):
        os.environ['PATH'] += os.pathsep + '/usr/local/bin'

    def test_verfication_without_metadata(self):
        manager = IDP_metadata_manger(None)
        pem_file = manager.get_trusted_pem_filename()
        verification = SAMLResposneSignatureVerification(pem_file, read_resource('SAMLResponse.txt'))
        self.assertFalse(verification.verify_signature())

    def test_verification_with_correct_metadata(self):
        manager = IDP_metadata_manger(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        pem_file = manager.get_trusted_pem_filename()
        verification = SAMLResposneSignatureVerification(pem_file, read_resource('SAMLResponse.txt'))
        self.assertTrue(verification.verify_signature())

    def test_verification_with_incorrect_response_format(self):
        manager = IDP_metadata_manger(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        pem_file = manager.get_trusted_pem_filename()
        verification = SAMLResposneSignatureVerification(pem_file, read_resource('SAMLResponse.xml'))
        self.assertFalse(verification.verify_signature())
# metadata = metadata = SAML_IDP_Metadata(create_xml_from_resources('IDP_Metadata.xml'))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
