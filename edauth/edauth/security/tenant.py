'''
Created on May 31, 2013

@author: dip
'''
import pyramid.threadlocal


def get_tenant_name(attributes):
    '''
    Returns the name of the tenant that the user belongs to
    Given the 'dn' from saml response, we grab the last 'ou' after we remove the base_dn
    '''
    tenant = None
    dn = attributes.get('dn')
    if dn is not None:
        value = dn[0]
        # Split the string into a list
        value = value.split(',')
        base_dn = (pyramid.threadlocal.get_current_registry().settings.get('base.dn')).split(',')
        # Reverse the two lists
        value.reverse()
        base_dn.reverse()
        while (0 < len(value) and 0 < len(base_dn)):
            # Strip out spaces
            if (value[0].replace(' ', '') == base_dn[0].replace(' ', '')):
                base_dn.pop(0)
                value.pop(0)
            else:
                break

        if len(value) > 0:
            element = value[0].split('=')
            # Ensure that it's an ou
            if element[0].lower() == 'ou':
                tenant = element[1]

    return tenant
