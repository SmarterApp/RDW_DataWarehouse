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
import os
import hashlib
from edauth.saml2.saml_idp_metadata_manager import IDP_metadata_manager


class Test(unittest.TestCase):

    def test_no_file_creation(self):
        manager = IDP_metadata_manager(None)
        self.assertIsNone(manager.get_trusted_pem_filename())

    def test_temp_file_management(self):
        manager = IDP_metadata_manager(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        temp_file = manager.get_trusted_pem_filename()
        self.assertTrue(os.path.exists(temp_file))
        manager = None
        self.assertFalse(os.path.exists(temp_file))

    def test_content_pem_file(self):
        pem_content = '''-----BEGIN CERTIFICATE-----
MIICQDCCAakCBEeNB0swDQYJKoZIhvcNAQEEBQAwZzELMAkGA1UEBhMCVVMxEzAR
BgNVBAgTCkNhbGlmb3JuaWExFDASBgNVBAcTC1NhbnRhIENsYXJhMQwwCgYDVQQK
EwNTdW4xEDAOBgNVBAsTB09wZW5TU08xDTALBgNVBAMTBHRlc3QwHhcNMDgwMTE1
MTkxOTM5WhcNMTgwMTEyMTkxOTM5WjBnMQswCQYDVQQGEwJVUzETMBEGA1UECBMK
Q2FsaWZvcm5pYTEUMBIGA1UEBxMLU2FudGEgQ2xhcmExDDAKBgNVBAoTA1N1bjEQ
MA4GA1UECxMHT3BlblNTTzENMAsGA1UEAxMEdGVzdDCBnzANBgkqhkiG9w0BAQEF
AAOBjQAwgYkCgYEArSQc/U75GB2AtKhbGS5piiLkmJzqEsp64rDxbMJ+xDrye0EN
/q1U5Of+RkDsaN/igkAvV1cuXEgTL6RlafFPcUX7QxDhZBhsYF9pbwtMzi4A4su9
hnxIhURebGEmxKW9qJNYJs0Vo5+IgjxuEWnjnnVgHTs1+mq5QYTA7E6ZyL8CAwEA
ATANBgkqhkiG9w0BAQQFAAOBgQB3Pw/UQzPKTPTYi9upbFXlrAKMwtFf2OW4yvGW
WvlcwcNSZJmTJ8ARvVYOMEVNbsT4OFcfu2/PeYoAdiDAcGy/F2Zuj8XJJpuQRSE6
PtQqBuDEHjjmOQJ0rV/r8mO1ZCtHRhpZ5zYRjhRC9eCbjx9VrFax0JDC/FfwWigm
rW0Y0Q==
-----END CERTIFICATE-----'''
        manager = IDP_metadata_manager(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        metadata_content_md5 = None
        with open(manager.get_trusted_pem_filename(), 'r') as f:
            m = hashlib.md5()
            data = f.read()
            m.update(data.replace('\n', '').encode())
            f.close()
            metadata_content_md5 = m.digest()
        m = hashlib.md5()
        m.update(pem_content.replace('\n', '').encode())
        pem_content_md5 = m.digest()
        self.assertEqual(pem_content_md5, metadata_content_md5)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
