'''
Created on Sep 19, 2013

@author: tosako
'''
from edauth.security.identity_parser import IdentityParser
from edauth.security.roles import Roles


class SbacIdentityParser(IdentityParser):
    CHAIN_ITEMS_COUNT = 17
    TENANT_INDEX = 8
    ROLE_INDEX = 2
    '''
    format of string in memberOf
    0 1      2    3     4        5      6              7              8      9     10                 11               12         13       14                    15                 16             17
     |RoleId|Name|Level|ClientID|Client|GroupOfStateID|GroupOfStates|StateID|State|GroupOfDistrictsID|GroupOfDistricts|DistrictID|District|GroupOfInstitutionsID|GroupOfInstitutions|InstitutionID|Institution|
    '''
    @staticmethod
    def get_roles(attributes):
        '''
        find roles from Attributes Element (SAMLResponse)
        '''
        roles = SbacIdentityParser.parse_tenancy_chain(attributes, SbacIdentityParser.ROLE_INDEX)
        # Ensure that a user doesn't have a role that is not defined
        if Roles.has_undefined_roles(roles):
            roles.append(Roles.get_invalid_role())
        return roles

    @staticmethod
    def get_tenant_name(attributes):
        '''
        returns a list of tenant names (ex. StateIDs)
        '''
        values = SbacIdentityParser.parse_tenancy_chain(attributes, SbacIdentityParser.TENANT_INDEX)
        # Lower case the tenant name
        return [value.lower() for value in values]

    @staticmethod
    def parse_tenancy_chain(attributes, index):
        '''
        Parses tenancy chain from 'memberOf' attribute from SAML response and returns the value located at index
        '''
        memberOf = attributes.get("memberOf")
        results = []
        if memberOf:
            values = memberOf[0].split('|')
            for i in range(index, len(values) - 1, SbacIdentityParser.CHAIN_ITEMS_COUNT):
                results.append(values[i])
        return results
