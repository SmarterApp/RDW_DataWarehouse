'''
Created on Sep 19, 2013

@author: tosako
'''


class IdentityParser():
    '''
    Abstract class to parse AttributeMappings
    '''
    def __init__(self, attributes):
        self.attributes = attributes

    def get_roles(self):
        raise NotImplementedError("Should have implemented this")

    def get_tenant_name(self):
        raise NotImplementedError("Should have implemented this")

    def get_role_relationship_chain(self):
        raise NotImplementedError("Should have implemented this")
