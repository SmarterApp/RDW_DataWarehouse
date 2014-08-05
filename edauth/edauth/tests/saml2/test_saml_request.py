'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edauth.saml2.saml_request import SamlRequest, SamlAuthnRequest,\
    SamlLogoutRequest
from xml.dom.minidom import parseString
from edauth.security.utils import inflate_base64_decode


class SamlRequestTest(unittest.TestCase):

    def test_saml_request_uuid_creation(self):
        request = SamlRequest('issuer')
        self.assertIsNotNone(request.get_id())

    def test_encode_saml_request(self):
        request = SamlRequest('issuer')
        data = '<?xml version="1.0"?><xml:saml>Test</xml:saml>'
        encoded = request.format_request(parseString(data))
        self.assertEqual(encoded, {'SAMLRequest': 's6nIzbEqTszNsQtJLS6x0YdzAQ=='.encode()})

    def test_SamlAuthnRequest(self):
        issuer = 'http://IamIssuer.com'
        request = SamlAuthnRequest(issuer)
        params = request.generate_saml_request()
        str_decoded = inflate_base64_decode(params['SAMLRequest']).decode()
        self.assertTrue(str_decoded.find(issuer) > 0)

    def test_SamlLogoutRequest(self):
        issuer = 'http://iamSomeIssuer.net'
        session_id = '123'
        name_id = 'abc'
        request = SamlLogoutRequest(issuer, session_id, issuer, name_id)
        params = request.generate_saml_request()
        str_decoded = inflate_base64_decode(params['SAMLRequest']).decode()
        expected_issuer = '<saml2:Issuer xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion">' + issuer + '</saml2:Issuer>'
        expected_session = '<saml2p:SessionIndex>' + session_id + '</saml2p:SessionIndex>'
        expected_name_id = '>' + name_id + '</saml2:NameID>'
        self.assertTrue(str_decoded.find(expected_issuer) > 0)
        self.assertTrue(str_decoded.find(expected_session) > 0)
        self.assertTrue(str_decoded.find(expected_name_id) > 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
