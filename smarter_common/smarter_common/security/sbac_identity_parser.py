'''
Created on Sep 19, 2013

@author: tosako
'''
from edauth.security.identity_parser import IdentityParser
from edauth.security.user import RoleRelation
import uuid
from edauth.security.session import Session


class SbacIdentityParser(IdentityParser):
    CHAIN_ITEMS_COUNT = 17
    ROLE_INDEX = 1
    TENANT_INDEX = 7
    STATE_CODE_INDEX = 8
    DISTRICT_ID_INDEX = 11
    SCHOOL_ID_INDEX = 15
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
        return _extract_role_relationship_chain(attributes.get('memberOf', []))

    @staticmethod
    def create_session(name, session_index, attributes, last_access, expiration):
        '''
        populate session from SAMLResponse
        '''
        # make a UUID based on the host ID and current time
        __session_id = str(uuid.uuid4())

        # get Attributes
        __attributes = attributes
        __name_id = name
        session = Session()
        session.set_session_id(__session_id)
        session.set_name_id(__name_id)
        # get fullName
        fullName = __attributes.get('fullName')
        if fullName is not None:
            session.set_fullName(fullName[0])

        # get firstName
        firstName = __attributes.get('firstName')
        if firstName is not None:
            session.set_firstName(firstName[0])

        # get lastName
        lastName = __attributes.get('lastName')
        if lastName is not None:
            session.set_lastName(lastName[0])

        # get uid
        if 'uid' in __attributes:
            if __attributes['uid']:
                session.set_uid(__attributes['uid'][0])

        # get guid
        guid = __attributes.get('guid')
        if guid is not None:
            session.set_guid(guid[0])

        # get Identity specific parsing values
        session.set_user_context(SbacIdentityParser.get_role_relationship_chain(__attributes))

        session.set_expiration(expiration)
        session.set_last_access(last_access)

        # get auth response session index that identifies the session with identity provider
        session.set_idp_session_index(session_index)

        return session


class SbacOauthIdentityParser(IdentityParser):
    '''
    format of string in sbac chain
     0      1    2     3        4      5              6             7       8     9                  10               11         12       13                    14                  15            16
    |RoleId|Name|Level|ClientID|Client|GroupOfStateID|GroupOfStates|StateID|State|GroupOfDistrictsID|GroupOfDistricts|DistrictID|District|GroupOfInstitutionsID|GroupOfInstitutions|InstitutionID|Institution|
    '''
    @staticmethod
    def get_role_relationship_chain(attributes):
        '''
        Returns a list of role/relationship
        '''
        # We get a string with all the tenancy chain separated by a comma
        chain = attributes.get("sbacTenancyChain").split(',') if attributes.get("sbacTenancyChain") else []
        return _extract_role_relationship_chain(chain)

    @staticmethod
    def create_session(name, session_index, attributes, last_access, expiration):
        '''
        populate session from SAMLResponse
        '''
        # make a UUID based on the host ID and current time
        __session_id = str(uuid.uuid4())

        # get Attributes
        __attributes = attributes
        __name_id = name
        session = Session()
        session.set_session_id(__session_id)
        session.set_name_id(__name_id)

        # get guid
        guid = __attributes.get('sbacUUID')
        if guid is not None:
            session.set_guid(guid)

        # get Identity specific parsing values
        session.set_user_context(SbacOauthIdentityParser.get_role_relationship_chain(__attributes))

        session.set_expiration(expiration)
        session.set_last_access(last_access)

        # get auth response session index that identifies the session with identity provider
        session.set_idp_session_index(session_index)

        return session


def _extract_role_relationship_chain(chains):
    '''
    Returns a list of role/relationship
    '''
    relations = []
    for chain in chains:
        tenancy_chain = [item if len(item) > 0 else None for item in chain.split('|')]
        # remove first and last items as they're always blank strings
        tenancy_chain.pop(0)
        tenancy_chain.pop()

        role = tenancy_chain[SbacIdentityParser.ROLE_INDEX]
        relations.append(RoleRelation(role, tenancy_chain[SbacIdentityParser.TENANT_INDEX], tenancy_chain[SbacIdentityParser.STATE_CODE_INDEX],
                         tenancy_chain[SbacIdentityParser.DISTRICT_ID_INDEX], tenancy_chain[SbacIdentityParser.SCHOOL_ID_INDEX]))
    return relations
