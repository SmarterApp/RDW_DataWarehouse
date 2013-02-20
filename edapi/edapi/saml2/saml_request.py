'''
Created on Feb 13, 2013

@author: dip
'''
from xml.dom.minidom import Document
import uuid
from time import gmtime, strftime
import zlib
import base64


class SamlRequest:
    '''Represents a SamlRequest'''

    def __init__(self, issuer_name):
        # UUID based on host ID and current time, or use 4 to get random
        self._uuid = str(uuid.uuid1())
        self._issuer_name = issuer_name

    def format_request(self, doc):
        # Seriailize the doc's root element so that it will strip out the xml declaration
        data = doc.documentElement.toxml('utf-8')
        return self.__deflate_base64_encode(data)

    # Deflate, base64 encode a byte string representing a SAMLRequest
    def __deflate_base64_encode(self, data):
        compressed = zlib.compress(data)
        # Strip away the first 2 bytes (header) and 4 bytes (checksum)
        encoded = base64.b64encode(compressed[2:-4])
        return {'SAMLRequest': encoded}

    def get_id(self):
        return self._uuid


class SamlAuthnRequest(SamlRequest):
    '''Represents a Saml AuthnRequest for Login'''

    def __init__(self, issuer_name):
        super().__init__(issuer_name)

    # Create XML SAML Auth Request
    # returns a byte string of a SAML AuthnRequest
    def generate_saml_request(self):
        doc = Document()
        samlp_auth_request = doc.createElement('samlp:AuthnRequest')
        samlp_auth_request.setAttribute('xmlns:samlp', 'urn:oasis:names:tc:SAML:2.0:protocol')
        samlp_auth_request.setAttribute('xmlns:saml', 'urn:oasis:names:tc:SAML:2.0:assertion')
        samlp_auth_request.setAttribute('ID', self._uuid)
        samlp_auth_request.setAttribute('Version', '2.0')
        samlp_auth_request.setAttribute('IssueInstant', strftime('%Y-%m-%dT%H:%M:%S', gmtime()))
        samlp_auth_request.setAttribute('AssertionConsumerServiceIndex', '0')
        samlp_auth_request.setAttribute('AttributeConsumingServiceIndex', '0')

        saml_issuer = doc.createElement('saml:Issuer')
        saml_issuer_text = doc.createTextNode(self._issuer_name)
        saml_issuer.appendChild(saml_issuer_text)
        samlp_auth_request.appendChild(saml_issuer)

        samlp_name_id_policy = doc.createElement('samlp:NameIDPolicy')
        samlp_name_id_policy.setAttribute('AllowCreate', 'true')
        samlp_name_id_policy.setAttribute('Format', 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient')
        samlp_auth_request.appendChild(samlp_name_id_policy)

        doc.appendChild(samlp_auth_request)

        return self.format_request(doc)


class SamlLogoutRequest(SamlRequest):
    '''Represents a Saml LogoutRequest'''

    def __init__(self, issuer_name, session_index, name_qualifier):
        super().__init__(issuer_name)
        self._session_index = session_index
        self._name_qualifier = name_qualifier

    def generate_saml_request(self):
        doc = Document()

        samlp_logout_request = doc.createElement('saml2p:SamlLogoutRequest')
        samlp_logout_request.setAttribute('xmlns:saml2p', 'urn:oasis:names:tc:SAML:2.0:protocol')
        samlp_logout_request.setAttribute('ID', self._uuid)
        samlp_logout_request.setAttribute('Version', '2.0')
        samlp_logout_request.setAttribute('IssueInstant', strftime('%Y-%m-%dT%H:%M:%S', gmtime()))

        saml_issuer = doc.createElement('saml2:Issuer')
        saml_issuer.setAttribute('xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion')
        saml_issuer_text = doc.createTextNode(self._issuer_name)
        saml_issuer.appendChild(saml_issuer_text)
        samlp_logout_request.appendChild(saml_issuer)

        samlp_name_id = doc.createElement('saml2:NameID')
        samlp_name_id.setAttribute('xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion')
        samlp_name_id.setAttribute('NameQualifier', self._name_qualifier)
        samlp_name_id.setAttribute('Format', 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient')
        samlp_name_id_text = doc.createTextNode('iTOWZVDc4u3txlVB/RJMMw5ZSAPW')
        samlp_name_id.appendChild(samlp_name_id_text)
        samlp_logout_request.appendChild(samlp_name_id)

        samlp_session_index = doc.createElement('saml2p:SessionIndex')
        samlp_session_index_text = doc.createTextNode(self._session_index)
        samlp_session_index.appendChild(samlp_session_index_text)
        samlp_logout_request.appendChild(samlp_session_index)

        doc.appendChild(samlp_logout_request)

        return self.format_request(doc)
