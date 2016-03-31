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
from xml.dom.minidom import Node


class SAML_IDP_Metadata():
    '''
    Parses SAML IDP Metadata and stores it as a DOM
    '''
    def __init__(self, idp_metadata_dom):
        self.__entityID = None
        self.__x509Certificate = None
        self.__metadata_ok = False
        if idp_metadata_dom is not None:
            self.__parse(idp_metadata_dom)
            self.__metadata_ok = True

    def __parse(self, idp_metadata_dom):
        __EntityDescriptor_node = idp_metadata_dom.childNodes[0]
        self.__entityID = __EntityDescriptor_node.getAttribute('entityID')
        __IDPSSODescriptor_node = self.__get_node(__EntityDescriptor_node, 'IDPSSODescriptor')
        if __IDPSSODescriptor_node is not None:
            __KeyDescriptor_node = self.__get_node(__IDPSSODescriptor_node, 'KeyDescriptor')
            if __KeyDescriptor_node is not None:
                __KeyInfo_node = self.__get_node(__KeyDescriptor_node, 'KeyInfo')
                if __KeyInfo_node is not None:
                    __X509Data_node = self.__get_node(__KeyInfo_node, 'X509Data')
                    if __X509Data_node is not None:
                        __X509Certificate_node = self.__get_node(__X509Data_node, 'X509Certificate')
                        if __X509Certificate_node is not None:
                            data = __X509Certificate_node.childNodes[0].data
                            # remove if data starts with \n
                            while data[0:1] == '\n' or data[0:1] == " ":
                                data = data[1:]
                            # remove any white space or '\n' at the end of ceriticate string
                            while data[-1:] == '\n' or data[-1:] == " ":
                                data = data[:-1]
                            self.__x509Certificate = data

    def __get_node(self, parent_node, node_name):
        for child_node in parent_node.childNodes:
            if child_node.nodeType == Node.ELEMENT_NODE:
                if child_node.localName == node_name:
                    return child_node
        return None

    def get_entityID(self):
        '''
        return entityId
        '''
        return self.__entityID

    def get_X509Certificate(self):
        '''
        return X509Certificate
        '''
        return self.__x509Certificate

    def is_metadata_ok(self):
        return self.__metadata_ok
