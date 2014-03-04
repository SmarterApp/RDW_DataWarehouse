'''
Created on Sep 19, 2013

@author: tosako
'''
from edauth.security.identity_parser import IdentityParser
from edauth.security.user import RoleRelation


class SbacIdentityParser(IdentityParser):
    CHAIN_ITEMS_COUNT = 17
    ROLE_INDEX = 1
    TENANT_INDEX = 7
    STATE_CODE_INDEX = 8
    DISTRICT_GUID_INDEX = 11
    SCHOOL_GUID_INDEX = 15
    '''
    format of string in memberOf
     0      1    2     3        4      5              6             7       8     9                  10               11         12       13                    14                  15            16
    |RoleId|Name|Level|ClientID|Client|GroupOfStateID|GroupOfStates|StateID|State|GroupOfDistrictsID|GroupOfDistricts|DistrictID|District|GroupOfInstitutionsID|GroupOfInstitutions|InstitutionID|Institution|
    '''
    @staticmethod
    def get_role_relationship_chain(attributes):
        '''
        Returns a list of role/relationship
        '''
        memberOf = attributes.get('memberOf')
        tenancy_chain = []
        if memberOf:
            tenancy_chain = memberOf[0].split('|')
            # remove first and last items as they're always blank strings
            tenancy_chain.pop(0)
            tenancy_chain.pop()
        relations = []
        for i in range(0, len(tenancy_chain), SbacIdentityParser.CHAIN_ITEMS_COUNT):
            relations.append(RoleRelation(tenancy_chain[SbacIdentityParser.ROLE_INDEX + i], tenancy_chain[SbacIdentityParser.TENANT_INDEX + i], tenancy_chain[SbacIdentityParser.STATE_CODE_INDEX + i],
                             tenancy_chain[SbacIdentityParser.DISTRICT_GUID_INDEX + i], tenancy_chain[SbacIdentityParser.SCHOOL_GUID_INDEX + i]))
        return relations
