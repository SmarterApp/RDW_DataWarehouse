'''
Created on Sep 19, 2013

@author: tosako
'''
from edauth.security.identity_parser import IdentityParser
from edauth.security.roles import Roles


class SbacIdentityParser(IdentityParser):
    '''
    format of string in memberOf
    0 1    2     3        4      5                  6                7              8             9       10    11                 12               13         14       15                    16                  17            18
     |Role|Level|ClientID|Client|AssociatedEntityID|AssociatedEntity|GroupOfStateID|GroupOfStates|StateID|State|GroupOfDistrictsID|GroupOfDistricts|DistrictID|District|GroupOfInstitutionsID|GroupOfInstitutions|InstitutionID|Institution
    '''
    @staticmethod
    def get_roles(attributes):
        '''
        find roles from Attributes Element (SAMLResponse)
        '''
        roles = []
        memberOf = attributes.get("memberOf", None)
        if memberOf is not None:
            value = memberOf[0]
            values = value.split('|')
            # this is temporary for testing.
            # remove temp_role when we have users with correct roles.
            temp_role = values[1]
            if temp_role == "Test Administrator":
                temp_role = "TEACHER"
            roles.append(temp_role)
        # If user has no roles or has a role that is not defined
        if not roles or Roles.has_undefined_roles(roles):
            roles.append(Roles.get_invalid_role())
        return roles

    @staticmethod
    def get_tenant_name(attributes):
        tenant = None
        memberOf = attributes.get('memberOf')
        if memberOf is not None:
            value = memberOf[0]
            # Split the string into a list
            value = value.split('|')
            #index 0 is always empty.
            #Tenant is always at index 10
            tenant = value[10].lower()
        return tenant
