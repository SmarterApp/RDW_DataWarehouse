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
Created on Feb 26, 2013

@author: tosako
'''
from xml.dom.minidom import parseString
from edauth.saml2.saml_response import SAMLResponse
from edauth.saml2.saml_response_signature_verification import SAMLResposneSignatureVerification
import time
import calendar


class SAMLResponseManager():
    '''
    Managing SAMLResponse - verify signature, check time condition
    and status.
    '''
    def __init__(self, saml_response_string):
        self.__saml_response = None
        self.__saml_string = saml_response_string
        if saml_response_string is not None:
            response_dom = parseString(self.__saml_string)
            self.__saml_response = SAMLResponse(response_dom)

    def get_SAMLResponse(self):
        '''
        return SAMLResponse class
        '''
        return self.__saml_response

    def is_signature_ok(self, trusted_pem_file):
        '''
        verify XML security
        including X509, DigestValue, SignatureValue
        '''
        sigver = SAMLResposneSignatureVerification(trusted_pem_file, self.__saml_string)
        return sigver.verify_signature()

    def is_auth_request_id_ok(self, auth_request_id):
        '''
        check auth request id against Reponse ID
        '''
        return self.__saml_response is not None and auth_request_id == self.__saml_response.get_InResponseTo()

    def is_status_ok(self):
        '''
        status code must be Sucess
        '''
        result = False
        if self.__saml_response is not None:
            status = self.__saml_response.get_status()
            if status is not None:
                status_code = status.get_status_code()
                result = status_code[-7:] == "Success"
        return result

    def is_condition_ok(self):
        '''
        check datetime condition
        '''
        result = True
        if self.__saml_response is not None:
            conditions = self.__saml_response.get_assertion().get_conditions()
            current_utc_time = calendar.timegm(time.gmtime())
            notBefore_utc = time_convert_utc(conditions.get_notBefore())
            notOnOrAfter_utc = time_convert_utc(conditions.get_notOnOrAfter())
            if notBefore_utc is None or current_utc_time < notBefore_utc:
                result = False
            elif notOnOrAfter_utc is None or current_utc_time >= notOnOrAfter_utc:
                result = False
        else:
            result = False
        return result


def time_convert_utc(datetime):
    '''
    support only UTC datetime format
    datetime must end with Z
    '''
    # if time is in UTC
    current_time_utc = None
    if datetime.endswith('Z'):
        current_time_utc = calendar.timegm(time.strptime(datetime[:-1], '%Y-%m-%dT%H:%M:%S'))
    return current_time_utc
