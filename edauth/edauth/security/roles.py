'''
Created on Feb 14, 2013

@author: dip
'''
from edauth import utils


class Roles:
    defined_permissions = {}
    # Pre-Populate a role of none
    defined_roles = utils.enum(NONE='NONE')

    @staticmethod
    def set_roles(mappings):
        '''
        Sets the roles.
        Mappings is a list of tuples of the form [(Allow, 'role_name', ('permissions'))]
        TODO:  We probably don't need to make it as an enum anymore
        '''
        Roles.acl = mappings
        roles = {}
        permissions = {}
        for mapping in mappings:
            role = mapping[1].upper()
            permission = mapping[2]
            roles[role] = role
            permissions[role] = permission
        # Make sure we have a role of None
        if 'NONE' not in roles.keys():
            roles['NONE'] = 'NONE'
        Roles.defined_roles = utils.enum(**roles)
        Roles.defined_permissions = permissions

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

    @staticmethod
    def has_permission(roles, permission):
        for role in roles:
            permissions = Roles.defined_permissions.get(role)
            if permissions and permission in permissions:
                return True
        return False

    @staticmethod
    def has_display_home_permission(roles):
        return Roles.has_permission(roles, 'display_home')
