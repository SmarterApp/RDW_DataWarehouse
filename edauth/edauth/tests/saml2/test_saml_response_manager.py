'''
Created on Feb 26, 2013

@author: tosako
'''
import unittest
from edauth.saml2.saml_response_manager import SAMLResponseManager,\
    time_convert_utc
from edauth.tests.test_helper.read_resource import read_resource
from edauth.saml2.saml_idp_metadata_manager import IDP_metadata_manager
import os


class Test(unittest.TestCase):

    def setUp(self):
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/local/bin'

    def test_get_SAMLResponse(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse.txt'))
        self.assertIsNotNone(manager)

    def test_is_signature_ok(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse.txt'))
        metadata_manager = IDP_metadata_manager(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'IDP_Metadata.xml')))
        self.assertTrue(manager.is_signature_ok(metadata_manager.get_trusted_pem_filename()))

    def test_is_auth_request_id_ok(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse.txt'))
        self.assertTrue(manager.is_auth_request_id_ok('334f96ca-7e00-11e2-b46e-3c07546832b4'))
        self.assertFalse(manager.is_auth_request_id_ok('asdfdelfalsdbflakeflkajsdlfjalskjfelkajsle'))

    def test_is_status_ok(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse.txt'))
        self.assertTrue(manager.is_status_ok())

    def test_is_not_status_ok(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse_response_not_ok.txt'))
        self.assertFalse(manager.is_status_ok())

    def test_time_convert_utc(self):
        mytime = "2013-02-23T21:40:33Z"
        utc = time_convert_utc(mytime)
        self.assertEqual(1361655633, utc)

    def test_is_condition_not_ok1(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse.txt'))
        self.assertFalse(manager.is_condition_ok())

    def test_is_condition_not_ok2(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse_time_test2.txt'))
        self.assertFalse(manager.is_condition_ok())

    def test_condition_ok(self):
        manager = SAMLResponseManager(read_resource('SAMLResponse_time_test1.txt'))
        self.assertTrue(manager.is_condition_ok())

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
