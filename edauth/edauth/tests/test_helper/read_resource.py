'''
Created on Feb 25, 2013

@author: tosako
'''
import os
from xml.dom.minidom import parse
from edauth.saml2.saml_response import SAMLResponse


def create_xml_from_resources(xml_file_name):
    xml_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', xml_file_name))
    dom = parse(xml_file)
    return dom


def create_SAMLResponse(xml_file_name):
    __dom_SAMLResponse = create_xml_from_resources(xml_file_name)
    samlResponse = SAMLResponse(__dom_SAMLResponse)
    return samlResponse


def read_resource(filename):
    data = None
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', filename)), 'r') as f:
        data = f.read()
        f.close()
    return data
