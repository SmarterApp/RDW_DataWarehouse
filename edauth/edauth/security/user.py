'''
Created on Mar 14, 2013

@author: dip
'''
from edauth.security.roles import Roles
import json
from edauth.security.utils import SetEncoder


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
    DISPLAYHOME = 'displayHome'


class RoleRelation(object):
    '''
    Role/Relationship information
    '''
    def __init__(self, role, tenant, state_code, district_guid, school_guid):
        self.role = role
        self.tenant = tenant
        self.state_code = state_code
        self.district_guid = district_guid
        self.school_guid = school_guid


class UserContext(object):
    '''
    Entity Relationship information that can represent user context
    '''
    def __init__(self, role_inst_rel_list):
        '''
        Instantiates user context from RoleRelation array. We do not preserve inter-relationships between institutions
        '''
        self.__tenant_context_map = {row.tenant: {} for row in role_inst_rel_list}
        for row in role_inst_rel_list:
            tenant = self.__tenant_context_map.get(row.tenant)
            role = tenant.get(row.role)
            role = {'sc': set(), 'dg': set(), 'sg': set()} if role is None else role
            role.get('sc').add(row.state_code)
            role.get('dg').add(row.district_guid)
            role.get('sg').add(row.school_guid)
            tenant[row.role] = role
            self.__tenant_context_map[row.tenant] = tenant

    def get_states(self, tenant, role):
        return self.__tenant_context_map[tenant][role]['sc']

    def get_districts(self, tenant, role):
        return self.__tenant_context_map[tenant][role]['dg']

    def get_schools(self, tenant, role):
        return self.__tenant_context_map[tenant][role]['sg']

    def __json__(self, request):
        '''
        custom json serialization for this object used by pyramid
        '''
        # TODO: Sets are not serializable, so convert to List first.  If we're not using set, remove this
        return json.loads(json.dumps(self.__tenant_context_map, cls=SetEncoder))


class User(object):
    '''
    Represents User information
    '''
    def __init__(self):
        self.__initialize_default_values()

    def __json__(self, request):
        '''
        custom json serializer used by pyramid for the User class
        '''
        return self.__dict__

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
        self.__info[UserConstants.DISPLAYHOME] = False

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

    def set_context(self, context):
        self.user_context = UserContext(context)
        # For now set the roles and tenant like this to make everything continue to work
        roles = []
        tenants = []
        state_codes = []
        for c in context:
            roles.append(c.role)
            tenants.append(c.tenant)
            state_codes.append(c.state_code)
        # We need to make sure that there are we know about all the roles
        if Roles.has_undefined_roles(roles):
            roles.append(Roles.get_invalid_role())
        self.__info[UserConstants.ROLES] = roles
        self.__info[UserConstants.TENANT] = tenants
        self.__info[UserConstants.STATECODE] = state_codes
        # Check whether 'home' is enabled
        has_home = Roles.has_display_home_permission(roles)
        self.__info[UserConstants.DISPLAYHOME] = has_home

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
