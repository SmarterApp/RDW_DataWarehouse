'''
Created on Feb 16, 2013

@author: dip
'''
import unittest
from edapi.saml2.saml_request import SamlRequest, SamlAuthnRequest,\
    SamlLogoutRequest
import base64
import zlib
from xml.dom.minidom import parseString


def base64_decode_inflate(params):
    byte_request = params["SAMLRequest"]
    base_decoded = base64.b64decode(byte_request)
    return zlib.decompress(base_decoded, -15).decode()


class SamlRequestTest(unittest.TestCase):

    def test_saml_request_uuid_creation(self):
        request = SamlRequest("issuer")
        self.assertIsNotNone(request.get_id())

    def test_encode_saml_request(self):
        request = SamlRequest("issuer")
        data = '<?xml version="1.0"?><xml:saml>Test</xml:saml>'
        encoded = request.format_request(parseString(data))
        self.assertEqual(encoded, {"SAMLRequest": "s6nIzbEqTszNsQtJLS6x0YdzAQ==".encode()})

    def test_SamlAuthnRequest(self):
        issuer = "http://IamIssuer.com"
        request = SamlAuthnRequest(issuer)
        params = request.create_request()
        str_decoded = base64_decode_inflate(params)
        self.assertTrue(str_decoded.find(issuer) > 0)

    def test_SamlLogoutRequest(self):
        issuer = "http://iamSomeIssuer.net"
        session_id = "123"
        request = SamlLogoutRequest(issuer, session_id, issuer)
        params = request.create_request()
        str_decoded = base64_decode_inflate(params)
        expected_issuer = '<saml2:Issuer xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion">' + issuer + '</saml2:Issuer>'
        expected_session = '<saml2p:SessionIndex>' + session_id + '</saml2p:SessionIndex>'
        self.assertTrue(str_decoded.find(expected_issuer) > 0)
        self.assertTrue(str_decoded.find(expected_session) > 0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
