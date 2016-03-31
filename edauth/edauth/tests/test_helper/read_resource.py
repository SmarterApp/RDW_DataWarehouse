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
