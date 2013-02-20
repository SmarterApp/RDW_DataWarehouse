'''
Created on Feb 16, 2013

@author: tosako
'''
import unittest
import os
from xml.dom.minidom import parseString
from edapi.saml2.saml_response import SAMLResponse
from edapi.saml2.saml_auth import SamlAuth


class Test(unittest.TestCase):

    def test_saml_pass(self):
        auth_request_id = 's2c39419140bad5e9c015019bcaa49215bf00d0322'
        saml_response = create_SAMLResponse('SAMLResponse.xml')
        saml_auth = SamlAuth(saml_response, auth_request_id=auth_request_id)
        self.assertTrue(saml_auth.is_validate(), "SAML2 response is valid")

#    def test_saml_bad_request_id(self):
#        auth_request_bad_id = 's2c39419140bad5e9c015019bcaa49215bf00d0BAD'
#        saml_response = create_SAMLResponse('SAMLResponse.xml')
#        saml_auth = SamlAuth(saml_response, auth_request_id=auth_request_bad_id)
#        self.assertFalse(saml_auth.is_validate(), "SAML2 response is not valid")

    def test_sam_bad_status(self):
        auth_request_id = 's2c39419140bad5e9c015019bcaa49215bf00d0322'
        saml_response = create_SAMLResponse('SAMLResponse_fail_status.xml')
        saml_auth = SamlAuth(saml_response, auth_request_id=auth_request_id)
        self.assertFalse(saml_auth.is_validate(), "SAML2 response is not valid")


def create_SAMLResponse(file_name):
    saml_xml = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', file_name))
    with open(saml_xml, 'r') as f:
        xml = f.read()
    f.close()
    __dom_SAMLResponse = parseString(xml)
    samlResponse = SAMLResponse(__dom_SAMLResponse)
    return samlResponse


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
