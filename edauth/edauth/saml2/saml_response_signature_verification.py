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
