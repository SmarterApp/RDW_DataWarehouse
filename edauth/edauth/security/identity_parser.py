'''
Created on Sep 19, 2013

@author: tosako
'''


class IdentityParser():
    '''
    Abstract class to parse AttributeMappings
    '''
    @staticmethod
    def get_roles(attributes):
        raise NotImplementedError("Should have implemented this")

    @staticmethod
    def get_tenant_name(attributes):
        raise NotImplementedError("Should have implemented this")
