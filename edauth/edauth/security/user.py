'''
Created on Mar 14, 2013

@author: dip
'''
from edauth.security.roles import Roles
import json
from edauth.security.utils import SetEncoder, remove_duplicates_and_none_from_list
from copy import deepcopy
from edcore.security.tenant import get_all_state_codes, get_all_tenants


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
        self.__hierarchy_context_map = deepcopy(self.__tenant_context_map)
        for row in role_inst_rel_list:
            self.build_hierarchy(row)
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

    def get_states(self, tenant, role):
        return self.get_all_context(tenant, role).get('state_code')

    def get_districts(self, tenant, role):
        return self.get_all_context(tenant, role).get('district_guid')

    def get_schools(self, tenant, role):
        return self.get_all_context(tenant, role).get('school_guid')

    def get_all_context(self, tenant, role):
        return self.__tenant_context_map[tenant][role] if tenant in self.__tenant_context_map and role in self.__tenant_context_map[tenant] else {}

    def get_chain(self, tenant, permission, params):
        '''
        Given a request parameter, determine if the user has context to the next hierarchy down.
        Returns a dictionary object, with 'all', and 'guid' as key. {'all': True, 'guid': set()} if user can access everything in the next hierarchy.
        {'all': False, 'guid': {'23'}} if user any only see guid '23' in the next hierarchy

        :param string tenant:  name of the user's tenant
        :param string permission: permission that we're verifying
        :param dict params:  request parameter of report
        '''
        if tenant in self.__hierarchy_context_map and permission in self.__hierarchy_context_map[tenant]:
            for guid in ['schoolGuid', 'districtGuid', 'stateCode']:
                if params.get(guid):
                    return self.validate_hierarchy(tenant, permission, params, guid)
        return self._get_default_permission()

    def build_hierarchy(self, row):
        '''
        Give a role relation object, build the hierarchy of permission that user can see
        :param RoleRelation row:  the object that we're trying to add to the existing hierarchy context map
        '''
        tenant = self.__hierarchy_context_map.get(row.tenant)
        current = tenant.get(row.role, self._get_default_permission())
        tenant[row.role] = self._traverse_hierarchy(row, current)
        self.__hierarchy_context_map[row.tenant] = tenant

    def _traverse_hierarchy(self, role_rel, current):
        '''
        With a role relation object, traverse to append to the existing current hierarchy
        '''
        head = current
        for guid in [role_rel.state_code, role_rel.district_guid, role_rel.school_guid, None]:
            if guid:
                if current['guid'].get(guid) is None:
                    current['guid'][guid] = self._get_default_permission()
            else:
                current['guid'] = {}
                current['all'] = True
                break
            current = current['guid'].get(guid, self._get_default_permission())
        return head

    def _get_default_permission(self):
        '''
        Returns the default permission of a particular hierachy level, ie. user cannot see anything in the next level down.
        '''
        return {'all': False, 'guid': {}}

    def validate_hierarchy(self, tenant, permission, params, identifier):
        '''
        Given request parameters and the level that the user is trying to access, return dict object that dictates whether
        the user has context to the next level down
        '''
        current = self.__hierarchy_context_map[tenant][permission]
        hierarchy = ['stateCode', 'districtGuid', 'schoolGuid']
        idx = hierarchy.index(identifier)
        for i in hierarchy[0:idx + 1]:
            current = current['guid'].get(params.get(i), {})
            if not current or current.get('all'):
                break
        return {'all': current.get('all', False), 'guid': list(current.get('guid', {}).keys())}

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
        self.__info[UserConstants.TENANT] = []
        self.__info[UserConstants.STATECODE] = []
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
        role_inst_rel_list = []
        default_permission = Roles.get_default_permission()
        # Replace role with default role if the role is not in our defined list and clone every role relation with default Permission
        for rel_chain in role_inst_rel_list_all:
            if Roles.has_undefined_roles([rel_chain.role]):
                rel_chain.role = default_permission
            elif rel_chain.role != default_permission:
                appended_role_rel = RoleRelation(default_permission, rel_chain.tenant, rel_chain.state_code, rel_chain.district_guid, rel_chain.school_guid)
                role_inst_rel_list += self._populate_role_relation(appended_role_rel)
            role_inst_rel_list += self._populate_role_relation(rel_chain)
        # If there is no roles, set it to an invalid one so user can logout
        if not role_inst_rel_list:
            self._add_role(Roles.get_invalid_role())
        self.__context = UserContext(role_inst_rel_list)
        # Check whether 'home' is enabled
        self.__info[UserConstants.DISPLAYHOME] = Roles.has_display_home_permission(self.__info[UserConstants.ROLES])

    def _populate_role_relation(self, rel_chain):
        known_tenants = get_all_tenants()
        new_rel_list = []
        self._add_role(rel_chain.role)
        if rel_chain.tenant is None and rel_chain.state_code is None and rel_chain.district_guid is None and rel_chain.school_guid is None:
            # We need to create the rolerelation for consortium level for every tenant that we know of
            for tenant in known_tenants:
                new_rel_list.append(RoleRelation(rel_chain.role, tenant, None, None, None))
                self._add_tenant(tenant)
            self._add_state_code(get_all_state_codes())
        else:
            self._add_tenant(rel_chain.tenant)
            self._add_state_code(rel_chain.state_code)
            new_rel_list.append(rel_chain)
        return new_rel_list

    def _add_role(self, role):
        self.__info[UserConstants.ROLES].append(role)
        self.__info[UserConstants.ROLES] = remove_duplicates_and_none_from_list(self.__info[UserConstants.ROLES])

    def _add_tenant(self, tenant):
        self.__info[UserConstants.TENANT].append(tenant)
        self.__info[UserConstants.TENANT] = remove_duplicates_and_none_from_list(self.__info[UserConstants.TENANT])

    def _add_state_code(self, state_codes):
        if isinstance(state_codes, list):
            self.__info[UserConstants.STATECODE] += state_codes
        else:
            self.__info[UserConstants.STATECODE].append(state_codes)
        self.__info[UserConstants.STATECODE] = remove_duplicates_and_none_from_list(self.__info[UserConstants.STATECODE])

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
