'''
Created on Oct 22, 2015

@author: dip
'''
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.security.tenant import get_state_code_to_tenant_map_public_reports


class PublicDBConnection(EdCoreDBConnection):
    '''
    Used for public reports
    '''
    CONFIG_NAMESPACE = 'edware.public.db'

    def __init__(self, tenant=None, state_code=None):
        if tenant is None:
            _map = get_state_code_to_tenant_map_public_reports()
            tenant = _map.get(state_code)

        super().__init__(tenant=tenant, state_code=state_code)

    @staticmethod
    def get_namespace():
        '''
        Returns the namespace of smarter database connection
        '''
        return PublicDBConnection.CONFIG_NAMESPACE + '.'

    @staticmethod
    def get_datasource_name(tenant=None):
        '''
        Returns datasource name for a tenant
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return PublicDBConnection.get_namespace() + tenant

    @staticmethod
    def get_db_config_prefix(tenant=None):
        '''
        Returns database config prefix based on tenant name
        '''
        if tenant is None:
            # Returns None will raise an Exception in base class
            return None
        return PublicDBConnection.get_namespace() + tenant + '.'


class ReportingDbConnection():
    '''
    Used for routing between public and private dbs
    '''
    def __init__(self, tenant=None, state_code=None, is_public=False):
        '''
        :params str tenant:  Name of tenant
        :params str state_code name of state_code
        :params bool is_public.  True if we want to access de-identified datastore
        '''
        if is_public:
            self.db_conn = PublicDBConnection(tenant=tenant, state_code=state_code)
        else:
            self.db_conn = EdCoreDBConnection(tenant=tenant, state_code=state_code)

    def __enter__(self):
        return self.db_conn

    def __exit__(self, exc_type, value, tb):
        self.db_conn.close_connection()
