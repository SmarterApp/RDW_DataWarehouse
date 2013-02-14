from xml.dom.minidom import Document
import uuid
from time import gmtime, strftime
'''
Created on Feb 13, 2013

@author: dip
'''
import zlib
import base64


class SamlRequest:
    
    def __init__(self):
        # UUID based on host ID and current time, or use 4 to get random
        self._uuid = str(uuid.uuid1())
    
    # Create XML SAML Auth Request
    # returns a byte string of a SAML AuthnRequest
    def get_auth_request(self):
        doc = Document()
        samlp_auth_request = doc.createElement('samlp:AuthnRequest')
        samlp_auth_request.setAttribute('xmlns:samlp', "urn:oasis:names:tc:SAML:2.0:protocol")
        samlp_auth_request.setAttribute('xmlns:saml', "urn:oasis:names:tc:SAML:2.0:assertion")
        samlp_auth_request.setAttribute('ID', self._uuid)
        samlp_auth_request.setAttribute('Version', "2.0")
        samlp_auth_request.setAttribute('IssueInstant', strftime("%Y-%m-%dT%H:%M:%S", gmtime()))
        samlp_auth_request.setAttribute('AssertionConsumerServiceIndex', "0")
        samlp_auth_request.setAttribute("AttributeConsumingServiceIndex", "0")
    
        saml_issuer = doc.createElement("saml:Issuer")
        saml_issuer_text = doc.createTextNode("http://localhost:6543/sp.xml")
        saml_issuer.appendChild(saml_issuer_text)
        samlp_auth_request.appendChild(saml_issuer)
    
        samlp_name_id_policy = doc.createElement("samlp:NameIDPolicy")
        samlp_name_id_policy.setAttribute("AllowCreate", "true")
        samlp_name_id_policy.setAttribute("Format", "urn:oasis:names:tc:SAML:2.0:nameid-format:transient")
        samlp_auth_request.appendChild(samlp_name_id_policy)
    
        doc.appendChild(samlp_auth_request)
    
        # Seriailize the doc's root element so that it will strip out the xml declaration
        data = doc.documentElement.toxml('utf-8')
    
        return self.encode_saml_request(data)
    
    
    # Deflate, base64 encode a byte string representing a SAMLRequest
    def encode_saml_request(self, data):
        compressed = zlib.compress(data)
        # TODO comment on this
        encoded = base64.b64encode(compressed[2:-4])
        return {'SAMLRequest': encoded}
    
    def get_id(self):
        return self._uuid
