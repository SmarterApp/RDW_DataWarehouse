'''
Created on Sep 19, 2013

@author: tosako
'''


class IdentityParser():
    '''
    Abstract class to parse AttributeMappings
    '''
    @staticmethod
    def get_role_relationship_chain(attributes):
        raise NotImplementedError("Should have implemented this")
