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
import tempfile
import os
import subprocess
from subprocess import STDOUT
import traceback


class SAMLResposneSignatureVerification():
    '''
    Create temporary file to save SAMLResponse for verification
    '''
    def __init__(self, cert_pem_filename, saml_response_string):
        # create temp file for SAMLResponse
        fd, path = tempfile.mkstemp()
        self.cert_pem_filename = cert_pem_filename
        self.saml_response_path = path
        os.write(fd, saml_response_string.encode())
        os.close(fd)

    def __del__(self):
        os.unlink(self.saml_response_path)

    def get_file_name(self):
        return self.saml_response_path

    def verify_signature(self):
        verify = False
        if self.cert_pem_filename is not None and self.saml_response_path is not None:
            cmd = ['xmlsec1', '--verify', '--id-attr:ID', 'urn:oasis:names:tc:SAML:2.0:assertion:Assertion', '--trusted-pem', self.cert_pem_filename, self.saml_response_path]
            try:
                output = subprocess.check_output(cmd, stderr=STDOUT)
                tokens = output.decode('utf-8').split(os.linesep)
                for token in tokens:
                    if token == "OK":
                        verify = True
            except:
                traceback.print_exc()
                verify = False
        return verify
