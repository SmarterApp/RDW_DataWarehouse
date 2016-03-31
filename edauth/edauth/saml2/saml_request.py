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
Contains classes to build SAML request messages

Created on Feb 13, 2013

@author: dip
'''
from xml.dom.minidom import Document
import uuid
from time import gmtime, strftime
from edauth.security.utils import deflate_base64_encode


class SamlRequest:
    '''Represents a SamlRequest'''

    def __init__(self, issuer_name):
        '''
        UUID based on host ID and current time, or use 4 to get random
        '''
        self._uuid = str(uuid.uuid1())
        self._issuer_name = issuer_name

    def format_request(self, doc):
        '''
        Serialize the doc's root element so that it will strip out the xml declaration
        '''
        data = doc.documentElement.toxml('utf-8')
        return {'SAMLRequest': deflate_base64_encode(data)}

    def get_id(self):
        '''
        Return request id
        '''
        return self._uuid


class SamlAuthnRequest(SamlRequest):
    '''Represents a Saml AuthnRequest for Login'''

    def __init__(self, issuer_name):
        super().__init__(issuer_name)

    def generate_saml_request(self):
        '''
        Creates an XML SAML Auth Request. Returns a byte string of a SAML AuthnRequest.
        '''
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

    def __init__(self, issuer_name, session_index, name_qualifier, name_id):
        super().__init__(issuer_name)
        self._session_index = session_index
        self._name_qualifier = name_qualifier
        self._name_id = name_id

    def generate_saml_request(self):
        '''
        Creates an XML SAML Logout Request. Returns as a byte string.
        '''
        doc = Document()

        samlp_logout_request = doc.createElement('saml2p:LogoutRequest')
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
        samlp_name_id_text = doc.createTextNode(self._name_id)
        samlp_name_id.appendChild(samlp_name_id_text)
        samlp_logout_request.appendChild(samlp_name_id)

        samlp_session_index = doc.createElement('saml2p:SessionIndex')
        samlp_session_index_text = doc.createTextNode(self._session_index)
        samlp_session_index.appendChild(samlp_session_index_text)
        samlp_logout_request.appendChild(samlp_session_index)

        doc.appendChild(samlp_logout_request)

        return self.format_request(doc)
