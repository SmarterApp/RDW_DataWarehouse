from xml.dom.minidom import Document
import uuid
from time import gmtime, strftime
'''
Created on Feb 13, 2013

@author: dip
'''
import zlib
import urllib
import base64


# Create XML SAML Auth Request
# returns a byte string of a SAML AuthnRequest
def get_auth_request():
    doc = Document()
    # UUID based on host ID and current time, or use 4 to get random
    request_id = str(uuid.uuid1())
    samlp_Auth_Request = doc.createElement('samlp:AuthnRequest')
    samlp_Auth_Request.setAttribute('xmlns:samlp', "urn:oasis:names:tc:SAML:2.0:protocol")
    samlp_Auth_Request.setAttribute('xmlns:saml', "urn:oasis:names:tc:SAML:2.0:assertion")
    samlp_Auth_Request.setAttribute('ID', request_id)
    samlp_Auth_Request.setAttribute('Version', "2.0")
    samlp_Auth_Request.setAttribute('IssueInstant', strftime("%Y-%m-%dT%H:%M:%S", gmtime()))
    samlp_Auth_Request.setAttribute('AssertionConsumerServiceIndex', "0")
    samlp_Auth_Request.setAttribute("AttributeConsumingServiceIndex", "0")

    saml_issuer = doc.createElement("saml:Issuer")
    saml_issuer_text = doc.createTextNode("http://localhost:6543/sp.xml")
    saml_issuer.appendChild(saml_issuer_text)
    samlp_Auth_Request.appendChild(saml_issuer)

    samlp_name_id_policy = doc.createElement("samlp:NameIDPolicy")
    samlp_name_id_policy.setAttribute("AllowCreate", "true")
    samlp_name_id_policy.setAttribute("Format", "urn:oasis:names:tc:SAML:2.0:nameid-format:transient")
    samlp_Auth_Request.appendChild(samlp_name_id_policy)

    doc.appendChild(samlp_Auth_Request)

    # This will strip out the xml version text
    data = doc.documentElement.toxml('utf-8')

    return (request_id, encode_saml_request(data))


def encode_saml_request(data):
    compressed = zlib.compress(data)
    encoded = base64.b64encode(compressed[2:-4])
    return urllib.parse.urlencode({'SAMLRequest': encoded})
