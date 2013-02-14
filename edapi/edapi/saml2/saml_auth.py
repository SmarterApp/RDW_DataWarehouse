'''
Created on Feb 13, 2013

@author: tosako
'''
from xml.dom.minidom import parseString
from edapi.saml2.saml_response import SAMLResponse
from edapi.security.roles import Roles


class SamlAuth:
    def __init__(self, response, auth_request_id):
        self.__response = response
        self.__id = auth_request_id

    def is_validate(self):
        status = self.__resposne.get_status()
        status_code = status.get_status_code()
        if self.__id != self.__response.get_id():
            return False
        return status_code[-7:] == "Success"

    def get_role(self):
        return Roles.TEACHER

xml = '''<samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" ID="s242006af1c228c11bb10f535f54f92d3e522e640e" InResponseTo="aaf23196-1773-2113-474a-fe114412ab72" Version="2.0" IssueInstant="2013-02-13T22:07:58Z" Destination="http://localhost:6543/Hello_dip"><saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">http://edwappsrv4.poc.dum.edwdc.net:18080/opensso</saml:Issuer><samlp:Status xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
        <samlp:StatusCode  xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
            Value="urn:oasis:names:tc:SAML:2.0:status:Success">
        </samlp:StatusCode>
        </samlp:Status>
        <saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" ID="s231a488ee929ab3e5258981c76ae62e7cb71f77d3" IssueInstant="2013-02-13T22:07:58Z" Version="2.0">
            <saml:Issuer>http://edwappsrv4.poc.dum.edwdc.net:18080/opensso</saml:Issuer>
            <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                <ds:SignedInfo>
                    <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                    <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                    <ds:Reference URI="#s231a488ee929ab3e5258981c76ae62e7cb71f77d3">
                        <ds:Transforms>
                            <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                            <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                        </ds:Transforms>
                        <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                        <ds:DigestValue>owjgUr9muh1dUOEJhETTppZ0S2o=</ds:DigestValue>
                    </ds:Reference>
                </ds:SignedInfo>
                <ds:SignatureValue>
                    WJwK5O38t0t1n6iAzYpi1JxIjUGb7DP0XXk1R7sK61jf0qycf9ZDvMH+M6ITiep3nHaLnR+hpOxu
                    AwygustFS7ITo6Taakl0+/99CDWYH+u5NU1aNfJuGhOM41w6QqwkemroPN6NCX+XTSAbb8nThOvn
                    Ou8I57x0ZPWhlLawYc4=
                </ds:SignatureValue>
                <ds:KeyInfo>
                    <ds:X509Data>
                        <ds:X509Certificate>
                            MIICQDCCAakCBEeNB0swDQYJKoZIhvcNAQEEBQAwZzELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNh
                            bGlmb3JuaWExFDASBgNVBAcTC1NhbnRhIENsYXJhMQwwCgYDVQQKEwNTdW4xEDAOBgNVBAsTB09w
                            ZW5TU08xDTALBgNVBAMTBHRlc3QwHhcNMDgwMTE1MTkxOTM5WhcNMTgwMTEyMTkxOTM5WjBnMQsw
                            CQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEUMBIGA1UEBxMLU2FudGEgQ2xhcmExDDAK
                            BgNVBAoTA1N1bjEQMA4GA1UECxMHT3BlblNTTzENMAsGA1UEAxMEdGVzdDCBnzANBgkqhkiG9w0B
                            AQEFAAOBjQAwgYkCgYEArSQc/U75GB2AtKhbGS5piiLkmJzqEsp64rDxbMJ+xDrye0EN/q1U5Of+
                            RkDsaN/igkAvV1cuXEgTL6RlafFPcUX7QxDhZBhsYF9pbwtMzi4A4su9hnxIhURebGEmxKW9qJNY
                            Js0Vo5+IgjxuEWnjnnVgHTs1+mq5QYTA7E6ZyL8CAwEAATANBgkqhkiG9w0BAQQFAAOBgQB3Pw/U
                            QzPKTPTYi9upbFXlrAKMwtFf2OW4yvGWWvlcwcNSZJmTJ8ARvVYOMEVNbsT4OFcfu2/PeYoAdiDA
                            cGy/F2Zuj8XJJpuQRSE6PtQqBuDEHjjmOQJ0rV/r8mO1ZCtHRhpZ5zYRjhRC9eCbjx9VrFax0JDC
                            /FfwWigmrW0Y0Q==
                        </ds:X509Certificate>
                    </ds:X509Data>
                </ds:KeyInfo>
            </ds:Signature>
            <saml:Subject>
                <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:transient" NameQualifier="http://edwappsrv4.poc.dum.edwdc.net:18080/opensso">iTOWZVDc4u3txlVB/RJMMw5ZSAPW</saml:NameID>
                <saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
                    <saml:SubjectConfirmationData InResponseTo="aaf23196-1773-2113-474a-fe114412ab72" NotOnOrAfter="2013-02-13T22:17:58Z" Recipient="http://localhost:6543/Hello_dip"/>
                </saml:SubjectConfirmation>
            </saml:Subject>
            <saml:Conditions NotBefore="2013-02-13T21:57:58Z" NotOnOrAfter="2013-02-13T22:17:58Z">
                <saml:AudienceRestriction>
                    <saml:Audience>http://localhost:6543/sp.xml</saml:Audience>
                </saml:AudienceRestriction>
            </saml:Conditions>
            <saml:AuthnStatement AuthnInstant="2013-02-13T22:07:58Z" SessionIndex="s29eb4b669b0901b70bbf5efb9c63b89d4dd9e1e01"><saml:AuthnContext><saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml:AuthnContextClassRef></saml:AuthnContext></saml:AuthnStatement><saml:AttributeStatement>
            <saml:Attribute Name="username"><saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">Linda Kim</saml:AttributeValue></saml:Attribute></saml:AttributeStatement></saml:Assertion></samlp:Response>'''
