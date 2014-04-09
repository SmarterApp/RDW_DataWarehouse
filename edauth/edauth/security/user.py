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
            role = {'state_code': set(), 'district_guid': set(), 'school_guid': set()} if role is None else role
            if row.school_guid:
                role.get('school_guid').add(row.school_guid)
            elif row.district_guid:
                role.get('district_guid').add(row.district_guid)
            elif row.state_code:
                role.get('state_code').add(row.state_code)
            tenant[row.role] = role
            self.__tenant_context_map[row.tenant] = tenant
        self.build_chain(role_inst_rel_list)

    def get_states(self, tenant, role):
        return self.get_all_context(tenant, role).get('state_code', set())

    def get_districts(self, tenant, role):
        return self.get_all_context(tenant, role).get('district_guid', set())

    def get_schools(self, tenant, role):
        return self.get_all_context(tenant, role).get('school_guid', set())

    def get_all_context(self, tenant, role):
        return self.__tenant_context_map[tenant][role] if tenant in self.__tenant_context_map and role in self.__tenant_context_map[tenant] else {}

    def get_chain(self, tenant, permission, params):
        if params.get('schoolGuid') and permission in self._map[tenant]:
            if self.validate_hierarchy(tenant, permission, params, 'schoolGuid'):
                return self._map[tenant][permission]['schoolGuid']
        elif params.get('districtGuid') and permission in self._map[tenant]:
            if self.validate_hierarchy(tenant, permission, params, 'districtGuid'):
                return self._map[tenant][permission]['schoolGuid']
        elif params.get('stateCode') and permission in self._map[tenant]:
            if self.validate_hierarchy(tenant, permission, params, 'stateCode'):
                return self._map[tenant][permission]['districtGuid']
        return {'all': False, 'guid': set()}

    def build_chain(self, role_inst_rel_list):
        self._map = {row.tenant: {} for row in role_inst_rel_list}
        for row in role_inst_rel_list:
            tenant = self._map.get(row.tenant)
            role = tenant.get(row.role)
            role = {'stateCode': {'all': False, 'guid': set()}, 'districtGuid': {'all': False, 'guid': set()}, 'schoolGuid': {'all': False, 'guid': set()}} if role is None else role
            for i in [(row.state_code, 'stateCode'), (row.district_guid, 'districtGuid'), (row.school_guid, 'schoolGuid')]:
                guid = i[0]
                key = i[1]
                if guid and not role[key]['all']:
                    role[key]['guid'].add(guid)
                else:
                    self.__set_all_permission(role, key)
            tenant[row.role] = role
            self._map[row.tenant] = tenant
        return self._map

    def __set_all_permission(self, role, identifier):
        role[identifier]['all'] = True
        role[identifier]['guid'] = set()

    def validate_hierarchy(self, tenant, permission, params, identifier):
        hierarchy = ['schoolGuid', 'districtGuid', 'stateCode']
        index = hierarchy.index(identifier)
        rtn = True if index >= 0 else False
        for i in hierarchy[index:]:
            rtn = rtn and self.is_institution_accessible(tenant, permission, params.get(i), i)
        return rtn

    def is_institution_accessible(self, tenant, permission, request_guid, identifier):
        return request_guid in self._map[tenant][permission][identifier]['guid'] or self._map[tenant][permission][identifier]['all']

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
        for k, _ in self.__info.items():
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

    def set_context(self, role_inst_rel_list_all):
        # For now set the roles and tenant like this to make everything continue to work
        roles = set()
        tenants = set()
        state_codes = set()
        role_inst_rel_list = [rel_chain for rel_chain in role_inst_rel_list_all if not Roles.has_undefined_roles([rel_chain.role])]
        for rel_chain in role_inst_rel_list:
            roles.add(rel_chain.role)
            tenants.add(rel_chain.tenant)
            state_codes.add(rel_chain.state_code)
        # If there is no roles, set it to an invalid one so user can logout
        if not role_inst_rel_list:
            roles.add(Roles.get_invalid_role())
        self.__context = UserContext(role_inst_rel_list)
        self.__info[UserConstants.ROLES] = list(roles)
        self.__info[UserConstants.TENANT] = list(tenants)
        self.__info[UserConstants.STATECODE] = list(state_codes)
        # Check whether 'home' is enabled
        self.__info[UserConstants.DISPLAYHOME] = Roles.has_display_home_permission(roles)

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

    def get_context(self):
        return self.__context
