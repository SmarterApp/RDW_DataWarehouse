'''
Created on Feb 13, 2013

@author: tosako
'''
from xml.dom.minidom import Node


class SAMLResponse:
    def __init__(self, response_xml):
        self.__parse(response_xml)

    def __parse(self, __response_xml):
        # get parent Element "Response"
        __Response_node = __response_xml.childNodes[0]

        self.__ID = self.__get_value(__Response_node, "ID")
        self.__InResponseTo = self.__get_value(__Response_node, "InResponseTo")
        self.__Version = self.__get_value(__Response_node, "Version")
        self.__IssueInstant = self.__get_value(__Response_node, "IssueInstant")
        self.__Destination = self.__get_value(__Response_node, "Destination")

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
        return self.__ID

    def get_status(self):
        return self.__status

    def get_assertion(self):
        return self.__assertion

    class Issuer:
        def __init__(self, issuer_node):
            self.__issuer = issuer_node.childNodes[0].data

    class Status:
        def __init__(self, status_node):
            for node in status_node.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    if node.localName == "StatusCode":
                        self.__status = node.getAttribute("Value")
                        break

        def get_status_code(self):
            return self.__status

    class Assertion:
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
                            if node0.localName == "SubjectConfirmation":
                                self.__subjectConfirmation = SAMLResponse.Assertion.SubjectConfirmation(node0)
                    elif node.localName == "Conditions":
                        self.__conditions = SAMLResponse.Assertion.Conditions(node)
                    elif node.localName == "AttributeStatement":
                        for node0 in node.childNodes:
                            if node0.nodeType == Node.ELEMENT_NODE:
                                if node0.localName == "Attribute":
                                    attribute = SAMLResponse.Assertion.Attribute(node0)

                                    item = self.__attributes.get(attribute.get_name(), None)
                                    if item is None:
                                        self.__attributes[attribute.get_name()] = attribute.get_value()
                                    else:
                                        item.append(attribute.get_value())

        def get_attributes(self):
            return self.__attributes

        class SubjectConfirmation:
            def __init__(self, subjectConfirmation_node):
                self.__method = subjectConfirmation_node.getAttribute("Method")
                for node in subjectConfirmation_node.childNodes:
                    if node.nodeType == Node.ELEMENT_NODE:
                        if node.localName == "SubjectConfirmationData":
                            self.__inResponseTo = node.getAttribute("InResponseTo")
                            self.__notOnOrAfter = node.getAttribute("NotOnOrAfter")
                            self.__Recipient = node.getAttribute("Recipient")

        class Conditions:
            def __init__(self, condition_node):
                self.__notBefore = condition_node.getAttribute("NotBefore")
                self.__notOnOrAfter = condition_node.getAttribute("NotOnOrAfter")

        class Attribute:
            def __init__(self, attribute_node):
                self.__name = attribute_node.getAttribute("Name")
                for node in attribute_node.childNodes:
                    if node.nodeType == Node.ELEMENT_NODE:
                        if node.localName == "AttributeValue":
                            self.__attributeValue = node.childNodes[0].data

            def get_name(self):
                return self.__name

            def get_value(self):
                return self.__attributeValue
