'''
Created on Mar 14, 2013

@author: dip
'''
from edcore.security.tenant import get_state_code_mapping, get_tenant_map


class UserConstants():
    UID = 'uid'
    NAME = 'name'
    FULLNAME = 'fullName'
    FIRSTNAME = 'firstName'
    LASTNAME = 'lastName'
    ROLES = 'roles'
    TENANT = 'tenant'
    GUID = 'guid'
    STATECODE = 'stateCode'


class User(object):
    '''
    Represents User information
    '''
    def __init__(self):
        self.__initialize_default_values()

    def __str__(self):
        '''
        Returns uid of the user
        '''
        return self.__info['uid']

    def __initialize_default_values(self):
        self.__info = {}
        self.__info[UserConstants.NAME] = {UserConstants.FULLNAME: None, UserConstants.FIRSTNAME: None, UserConstants.LASTNAME: None}
        self.__info[UserConstants.UID] = None
        self.__info[UserConstants.ROLES] = []
        self.__info[UserConstants.TENANT] = None
        self.__info[UserConstants.GUID] = None

    def set_user_info(self, info):
        '''
        Given a dictionary, insert relevant values to self.__info
        @param info: user information
        @type info: dict
        '''
        for k, v in self.__info.items():
            value = info.get(k, None)
            if value is not None:
                self.__info[k] = value

    def set_name(self, name):
        '''
        @param name: the name to be set
        @type info: string
        '''
        self.__info[UserConstants.NAME] = name

    def set_uid(self, uid):
        '''
        @param uid: the uid to be set
        @type info: string
        '''
        self.__info[UserConstants.UID] = uid

    def set_full_name(self, full_name):
        '''
        @param full_name: the full name to be set
        @type info: string
        '''
        self.__info[UserConstants.NAME][UserConstants.FULLNAME] = full_name

    def set_first_name(self, first_name):
        '''
        @param first_name: the first name to be set
        @type info: string
        '''
        self.__info[UserConstants.NAME][UserConstants.FIRSTNAME] = first_name

    def set_last_name(self, last_name):
        '''
        @param last_name: the last name to be set
        @type info: string
        '''
        self.__info[UserConstants.NAME][UserConstants.LASTNAME] = last_name

    def set_roles(self, roles):
        '''
        @param roles: the roles to be set
        @type info: string
        '''
        self.__info[UserConstants.ROLES] = roles

    def set_tenants(self, tenants):
        '''
        @param tenant: the tenants to be set
        @type tenant: list
        '''
        if not isinstance(tenants, list):
            tenants = [tenants]
        # TODO:  This needs to be removed after SSO integration
        # Test code for multi-tenancy
        if 'CONSORTIUM_EDUCATION_ADMINISTRATOR_1' in self.get_roles():
            tenants = list(get_tenant_map().keys())
        self.__info[UserConstants.TENANT] = tenants
        # Set the state code based on tenant name
        self.__info[UserConstants.STATECODE] = get_state_code_mapping(tenants)

    def set_guid(self, guid):
        '''
        @param guid: the guid to set
        @type guid: string
        '''
        self.__info[UserConstants.GUID] = guid

    def get_name(self):
        return {UserConstants.NAME: self.__info[UserConstants.NAME]}

    def get_uid(self):
        return self.__info[UserConstants.UID]

    def get_user_context(self):
        return self.__info

    def get_roles(self):
        return self.__info[UserConstants.ROLES]

    def get_tenants(self):
        return self.__info[UserConstants.TENANT]

    def get_guid(self):
        return self.__info[UserConstants.GUID]
