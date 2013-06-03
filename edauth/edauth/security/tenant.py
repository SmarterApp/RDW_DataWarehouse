'''
Created on May 31, 2013

@author: dip
'''
import pyramid.threadlocal


def get_tenant_name(attributes):
    '''
    @param attributes:  A dictionary of attributes with values that are lists
    Returns the name of the tenant that the user belongs to in lower case, None if tenant is not found
    Given the 'dn' from saml response, we grab the last 'ou' after we remove the ldap_base_dn
    Sample value: 'cn=userName,ou=myOrg,ou=myCompany,dc=myDomain,dc=com'
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
                tenant = element[1]

    return tenant
