'''
Created on Feb 25, 2013

@author: tosako
'''
import tempfile
import os
from xml.dom.minidom import parse
from edauth.saml2.saml_idp_metadata import SAML_IDP_Metadata


class IDP_metadata_manager():
    '''
    IPD metadata manager class
    class SAML_IDP_Metadata is required for constructor
    '''
    def __init__(self, saml_idp_metadata_file_location):
        self.path = None
        if saml_idp_metadata_file_location is not None:
            self.SAML_IDP_Metadata = SAML_IDP_Metadata(parse(saml_idp_metadata_file_location))
            if self.SAML_IDP_Metadata.is_metadata_ok():
                self.__create_trusted_pem_file()

    def __del__(self):
        if self.path is not None:
            os.unlink(self.path)

    def __create_trusted_pem_file(self):
        fd, path = tempfile.mkstemp()
        self.path = path
        os.write(fd, '-----BEGIN CERTIFICATE-----\n'.encode())
        os.write(fd, self.SAML_IDP_Metadata.get_X509Certificate().encode())
        os.write(fd, '\n-----END CERTIFICATE-----'.encode())
        os.close(fd)

    def get_trusted_pem_filename(self):
        return self.path
