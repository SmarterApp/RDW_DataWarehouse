'''
Created on Sep 19, 2013

@author: tosako
'''
from edauth.security.identity_parser import IdentityParser
from edauth.security.roles import Roles
from edauth.security.user import RoleRelation


class SbacIdentityParser(IdentityParser):
    CHAIN_ITEMS_COUNT = 17
    ROLE_INDEX = 1
    TENANT_INDEX = 7
    STATE_CODE_INDEX  = 8
    DISTRICT_GUID_INDEX = 11
    SCHOOL_GUID_INDEX = 15
    '''
    format of string in memberOf
    0      1    2     3        4      5              6             7       8     9                  10               11         12       13                    14                  15            16
    RoleId|Name|Level|ClientID|Client|GroupOfStateID|GroupOfStates|StateID|State|GroupOfDistrictsID|GroupOfDistricts|DistrictID|District|GroupOfInstitutionsID|GroupOfInstitutions|InstitutionID|Institution
    '''
    def __init__(self, attributes):
        super().__init__(attributes)
        self.tenancy_chain = []
        memberOf = attributes.get('memberOf')
        if memberOf:
            self.tenancy_chain = memberOf[0].split('|')
            # remove first and last item as they're always blank strings
            self.tenancy_chain.pop(0)
            self.tenancy_chain.pop()

    def get_roles(self):
        '''
        find roles from Attributes Element (SAMLResponse)
        '''
        roles = self.parse_tenancy_chain(self.ROLE_INDEX)
        # Ensure that a user doesn't have a role that is not defined
        if Roles.has_undefined_roles(roles):
            roles.append(Roles.get_invalid_role())
        return roles

    def get_tenant_name(self):
        '''
        returns a list of tenant names (ex. StateIDs)
        '''
        values = self.parse_tenancy_chain( self.TENANT_INDEX)
        # Lower case the tenant name
        return [value.lower() for value in values]

    def parse_tenancy_chain(self, index):
        '''
        returns the value located at index in tenancy chain
        '''
        results = []
        for i in range(index, len(self.tenancy_chain), SbacIdentityParser.CHAIN_ITEMS_COUNT):
            results.append(self.tenancy_chain[i])
        return results

    def get_role_relationship_chain(self):
        '''
        Returns a list of role/relationship
        '''
        relations = []
        for i in range(0, len(self.tenancy_chain), SbacIdentityParser.CHAIN_ITEMS_COUNT):
            relations.append(RoleRelation(self.tenancy_chain[self.ROLE_INDEX + i], self.tenancy_chain[self.TENANT_INDEX + i], self.tenancy_chain[self.STATE_CODE_INDEX + i],
                             self.tenancy_chain[self.DISTRICT_GUID_INDEX + i], self.tenancy_chain[self.SCHOOL_GUID_INDEX + i]))
        return relations