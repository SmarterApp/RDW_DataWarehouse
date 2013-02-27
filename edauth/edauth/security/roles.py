'''
Created on Feb 14, 2013

@author: dip
'''
from edauth import utils


class Roles:
    # Pre-Populate a role of none
    defined_roles = utils.enum(NONE='NONE')

    @staticmethod
    def set_roles(mappings):
        '''
        Sets the roles
        mappings is a list of tuple of the form [(Allow, 'role_name', ('permissions'))]
        TODO:  We probably don't need to make it as an enum anymore
        '''
        kwargs = {}
        for mapping in mappings:
            role = mapping[1].upper()
            #permission = mapping[2]
            kwargs[role] = role
        # Make sure we have a role of None
        if 'NONE' not in kwargs.keys():
            kwargs['NONE'] = 'NONE'
        Roles.defined_roles = utils.enum(**kwargs)

    @staticmethod
    def get_invalid_role():
        '''
        Returns the value of a role of None (empty memberOf from SAML response)
        '''
        return Roles.defined_roles.NONE

    @staticmethod
    def has_undefined_roles(roles):
        '''
        Given a list of roles, return true if there is an unknown role
        '''
        for role in roles:
            if Roles.defined_roles.reverse_mapping.get(role) is None:
                return True
        return False
