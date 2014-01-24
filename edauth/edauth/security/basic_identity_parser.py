'''
Created on Sep 19, 2013

@author: tosako
'''

from edauth.security.identity_parser import IdentityParser
import pyramid
import re
from edauth.security.roles import Roles


class BasicIdentityParser(IdentityParser):
    @staticmethod
    def get_roles(attributes):
        '''
        find roles from Attributes Element (SAMLResponse)
        '''
        roles = []
        values = attributes.get("memberOf", None)
        if values is not None:
            for value in values:
                cn = re.search('cn=(.*?),', value.lower())
                if cn is not None:
                    role = cn.group(1).upper()
                    roles.append(role)
        # If user has no roles or has a role that is not defined
        if not roles or Roles.has_undefined_roles(roles):
            roles.append(Roles.get_invalid_role())
        return roles

    @staticmethod
    def get_tenant_name(attributes):
        '''
        Returns the name of the tenant that the user belongs to in lower case, None if tenant is not found.
        Given the 'dn' from saml response, we grab the last 'ou' after we remove the ldap_base_dn.
        Sample value: 'cn=userName,ou=myOrg,ou=myCompany,dc=myDomain,dc=com'
        :param attributes:  A dictionary of attributes with values that are lists
        '''
        tenant = None
        dn = attributes.get('dn')
        if dn is not None:
            value = dn[0].lower()
            # Split the string into a list
            value = value.split(',')
            ldap_base_dn = (pyramid.threadlocal.get_current_registry().settings.get('ldap.base.dn')).split(',')
            # Reverse the two lists
            value.reverse()
            ldap_base_dn.reverse()
            # Traverse through and pop elements that have the same value
            while (0 < len(value) and 0 < len(ldap_base_dn)):
                if (value[0] == ldap_base_dn[0]):
                    ldap_base_dn.pop(0)
                    value.pop(0)
                else:
                    break

            if (len(value) > 0 and len(ldap_base_dn) == 0):
                element = value[0].split('=')
                # Ensure that it's an ou
                if element[0] == 'ou':
                    # Return it as a list of one
                    tenant = [element[1]]

        return tenant
