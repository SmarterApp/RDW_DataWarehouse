from edauth.security.identity_parser import IdentityParser
from edauth.security.user import RoleRelation

__author__ = 'npandey'


class HPZIdentityParser(IdentityParser):

    @staticmethod
    def get_role_relationship_chain(attributes):
        '''
        Returns a list of role/relationship
        '''
        relations = [RoleRelation('General', '', '', '', '')]

        return relations
