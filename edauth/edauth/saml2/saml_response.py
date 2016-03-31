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
Created on Feb 13, 2013

@author: tosako
'''
from xml.dom.minidom import Node


class SAMLResponse:
    '''
    Parses SAML XML received from OpenAM
    '''
    def __init__(self, response_xml):
        self.__parse(response_xml)

    def __parse(self, __response_xml):
        '''
        get parent Element "Response
        '''
        __Response_node = __response_xml.childNodes[0]

        self.ID = self.__get_value(__Response_node, "ID")
        self.InResponseTo = self.__get_value(__Response_node, "InResponseTo")
        self.Version = self.__get_value(__Response_node, "Version")
        self.IssueInstant = self.__get_value(__Response_node, "IssueInstant")
        self.Destination = self.__get_value(__Response_node, "Destination")

        # get Issuer, Status, and Assertion element
        for node in __Response_node.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                if node.localName == "Issuer":
                    self.__issuer = SAMLResponse.Issuer(node)
                elif node.localName == "Status":
                    self.__status = SAMLResponse.Status(node)
                elif node.localName == "Assertion":
                    self.__assertion = SAMLResponse.Assertion(node)

    def __get_value(self, node, name):
        return node.getAttribute(name)

    def get_id(self):
        return self.ID

    def get_InResponseTo(self):
        return self.InResponseTo

    def get_status(self):
        return self.__status

    def get_assertion(self):
        return self.__assertion

    class Issuer:
        '''
        Issuer Element
        '''
        def __init__(self, issuer_node):
            self.__issuer = issuer_node.childNodes[0].data

    class Status:
        '''
        Status Element
        '''
        def __init__(self, status_node):
            for node in status_node.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    if node.localName == "StatusCode":
                        self.__status = node.getAttribute("Value")
                        break

        def get_status_code(self):
            return self.__status

    class Assertion:
        '''
        Assertion Element
        '''
        def __init__(self, assertion_node):
            self.__attributes = {}
            for node in assertion_node.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    if node.localName == "Issuer":
                        self.__issuer = SAMLResponse.Issuer(node)
                    elif node.localName == "Signature":
                        for node0 in node.childNodes:
                            if node0.nodeType == Node.ELEMENT_NODE:
                                if node0.localName == "SignatureValue":
                                    self.__signatureValuer = node0.childNodes[0].data
                                elif node0.localName == "KeyInfo":
                                    for node1 in node0.childNodes:
                                        if node1.nodeType == Node.ELEMENT_NODE:
                                            if node1.localName == "X509Data":
                                                for node2 in node1.childNodes:
                                                    if node2.nodeType == Node.ELEMENT_NODE:
                                                        if node2.localName == "X509Certificate":
                                                            self.__x509Certificate = node2.childNodes[0].data
                    elif node.localName == "Subject":
                        for node0 in node.childNodes:
                            if node0.localName == "NameID":
                                self.__name_id = node0.childNodes[0].data
                            elif node0.localName == "SubjectConfirmation":
                                self.__subjectConfirmation = SAMLResponse.Assertion.SubjectConfirmation(node0)
                    elif node.localName == "Conditions":
                        self.__conditions = SAMLResponse.Assertion.Conditions(node)
                    elif node.localName == "AttributeStatement":
                        for node0 in node.childNodes:
                            if node0.nodeType == Node.ELEMENT_NODE:
                                if node0.localName == "Attribute":
                                    attribute = SAMLResponse.Assertion.Attribute(node0)
                                    self.__attributes[attribute.get_name()] = attribute.get_value()
                    elif node.localName == "AuthnStatement":
                        self.__session_index = node.getAttribute("SessionIndex")

        def get_conditions(self):
            return self.__conditions

        def get_attributes(self):
            return self.__attributes

        def get_session_index(self):
            return self.__session_index

        def get_name_id(self):
            return self.__name_id

        class SubjectConfirmation:
            '''
            SubjectConfirmation Element
            '''
            def __init__(self, subjectConfirmation_node):
                self.__method = subjectConfirmation_node.getAttribute("Method")
                for node in subjectConfirmation_node.childNodes:
                    if node.nodeType == Node.ELEMENT_NODE:
                        if node.localName == "SubjectConfirmationData":
                            self.__inResponseTo = node.getAttribute("InResponseTo")
                            self.__notOnOrAfter = node.getAttribute("NotOnOrAfter")
                            self.__Recipient = node.getAttribute("Recipient")

        class Conditions:
            '''
            Condition Element
            '''
            def __init__(self, condition_node):
                self.__notBefore = condition_node.getAttribute("NotBefore")
                self.__notOnOrAfter = condition_node.getAttribute("NotOnOrAfter")

            def get_notBefore(self):
                return self.__notBefore

            def get_notOnOrAfter(self):
                return self.__notOnOrAfter

        class Attribute:
            '''
            Attribute Element
            '''
            def __init__(self, attribute_node):
                self.__name = attribute_node.getAttribute("Name")
                self.__attributeValue = []
                for node in attribute_node.childNodes:
                    if node.nodeType == Node.ELEMENT_NODE:
                        if node.localName == "AttributeValue":
                            self.__attributeValue.append(node.childNodes[0].data)

            def get_name(self):
                return self.__name

            def get_value(self):
                return self.__attributeValue
