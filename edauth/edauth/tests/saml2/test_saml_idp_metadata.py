'''
Created on Feb 25, 2013

@author: tosako
'''
import unittest
from edauth.saml2.saml_idp_metadata import SAML_IDP_Metadata
from edauth.tests.test_helper.read_resource import create_xml_from_resources


class Test(unittest.TestCase):

    def test_no_dom_input(self):
        no_saml_dom_metadata = SAML_IDP_Metadata(None)
        self.assertIsNone(no_saml_dom_metadata.get_entityID())
        self.assertIsNone(no_saml_dom_metadata.get_X509Certificate())
        self.assertFalse(no_saml_dom_metadata.is_metadata_ok())

    def test_parsed_metadata(self):
        expected_x509 = '''MIICQDCCAakCBEeNB0swDQYJKoZIhvcNAQEEBQAwZzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNh
bGlmb3JuaWExFDASBgNVBAcTC1NhbnRhIENsYXJhMQwwCgYDVQQKEwNTdW4xEDAOBgNVBAsTB09w
ZW5TU08xDTALBgNVBAMTBHRlc3QwHhcNMDgwMTE1MTkxOTM5WhcNMTgwMTEyMTkxOTM5WjBnMQsw
CQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEUMBIGA1UEBxMLU2FudGEgQ2xhcmExDDAK
BgNVBAoTA1N1bjEQMA4GA1UECxMHT3BlblNTTzENMAsGA1UEAxMEdGVzdDCBnzANBgkqhkiG9w0B
AQEFAAOBjQAwgYkCgYEArSQc/U75GB2AtKhbGS5piiLkmJzqEsp64rDxbMJ+xDrye0EN/q1U5Of+
RkDsaN/igkAvV1cuXEgTL6RlafFPcUX7QxDhZBhsYF9pbwtMzi4A4su9hnxIhURebGEmxKW9qJNY
Js0Vo5+IgjxuEWnjnnVgHTs1+mq5QYTA7E6ZyL8CAwEAATANBgkqhkiG9w0BAQQFAAOBgQB3Pw/U
QzPKTPTYi9upbFXlrAKMwtFf2OW4yvGWWvlcwcNSZJmTJ8ARvVYOMEVNbsT4OFcfu2/PeYoAdiDA
cGy/F2Zuj8XJJpuQRSE6PtQqBuDEHjjmOQJ0rV/r8mO1ZCtHRhpZ5zYRjhRC9eCbjx9VrFax0JDC
/FfwWigmrW0Y0Q=='''
        metadata = SAML_IDP_Metadata(create_xml_from_resources('IDP_Metadata.xml'))
        self.assertEqual('http://edwappsrv4.poc.dum.edwdc.net:18080/opensso', metadata.get_entityID())
        self.assertEqual(expected_x509, metadata.get_X509Certificate())
        self.assertTrue(metadata.is_metadata_ok())

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
