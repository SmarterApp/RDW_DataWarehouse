# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Mar 5, 2013

@author: tosako
'''
from edschema.database.connector import DBConnection
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from edschema.metadata.ed_metadata import generate_ed_metadata
from edcore.security.tenant import get_state_code_to_tenant_map


class EdCoreDBConnection(DBConnection):
    '''
    DBConnector for Smarter Project
    This is used for database connection for reports
    '''
    CONFIG_NAMESPACE = 'edware.db'

    def __init__(self, tenant=None, state_code=None):
        if tenant is None:
            # Get user's tenant from session
            __user = authenticated_userid(get_current_request())
            if __user:
                # User object has a list of tenant.
                tenants = __user.get_tenants()
                if len(tenants) > 0:
                    if len(tenants) is 1:
                        tenant = tenants[0]
                    else:
                        # Match tenant to the state code
                        _map = get_state_code_to_tenant_map()
                        tenant = _map.get(state_code)
        super().__init__(name=self.get_datasource_name(tenant))

    @staticmethod
    def get_namespace():
        '''
        Returns the namespace of smarter database connection
        '''
        return EdCoreDBConnection.CONFIG_NAMESPACE + '.'

    @staticmethod
    def get_datasource_name(tenant=None):
        '''
        Returns datasource name for a tenant
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return EdCoreDBConnection.get_namespace() + tenant

    @staticmethod
    def get_db_config_prefix(tenant=None):
        '''
        Returns database config prefix based on tenant name
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return EdCoreDBConnection.get_namespace() + tenant + '.'

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        '''
        Generates metadata for edware
        '''
        return generate_ed_metadata(schema_name=schema_name, bind=bind)
