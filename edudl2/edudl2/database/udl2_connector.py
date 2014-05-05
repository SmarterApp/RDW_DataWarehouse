from edudl2.database.metadata.udl2_metadata import generate_udl2_metadata
from edschema.database.connector import DBConnection
from edschema.database.generic_connector import setup_db_connection_from_ini
from sqlalchemy.sql.expression import text
__author__ = 'swimberly'
from edschema.metadata_generator import generate_ed_metadata


UDL_NAMESPACE = 'udl2_db_conn'
TARGET_NAMESPACE = 'target_db_conn'
PRODUCTION_NAMESPACE = 'prod_db_conn'
DEFAULT_TENANT = 'edware'


class UDL2DBConnection(DBConnection):
    """
    DBConnector for the UDL Database
    """
    def __init__(self, tenant=None, namespace=UDL_NAMESPACE):
        self.datasource_name = namespace + (('.' + tenant) if tenant else '')
        super().__init__(name=self.datasource_name)

    def get_namespace(self):
        return self.namespace

    def get_datasource_name(self):
        '''
        Returns datasource name for UDL Stats
        '''
        return self.datasource_name


def get_udl_connection():
    '''
    Get UDL connection
    '''
    return UDL2DBConnection(tenant=DEFAULT_TENANT, namespace=UDL_NAMESPACE)


def get_target_connection(tenant, schema_name=None):
    '''
    Get Target pre-prod connection
    '''
    conn = UDL2DBConnection(tenant=tenant, namespace=TARGET_NAMESPACE)
    if schema_name:
        conn.set_metadata_by_generate(schema_name, generate_ed_metadata)
    return conn


def get_prod_connection(tenant):
    '''
    Get production connection
    '''
    return UDL2DBConnection(tenant, namespace=PRODUCTION_NAMESPACE)


def initialize_db_udl(udl2_conf, allow_create_schema=False):
    initialize_db(UDL_NAMESPACE, generate_udl2_metadata, False, udl2_conf, allow_create_schema)


def initialize_db_target(udl2_conf):
    initialize_db(TARGET_NAMESPACE, generate_ed_metadata, True, udl2_conf)
    # Install dblink extension on preprod database if it doesn't exist
    for tenant in udl2_conf[TARGET_NAMESPACE]:
        with get_target_connection(tenant) as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS dblink"))


def initialize_db_prod(udl2_conf):
    initialize_db(PRODUCTION_NAMESPACE, generate_ed_metadata, True, udl2_conf)


def initialize_db(namespace, metadata_generator, allows_multiple_tenants, udl2_conf, allow_schema_create=False):
    """
    Setup connection for udl2
    :param connector:
    :param udl2_conf:
    :param allow_schema_create:
    :return:
    """
    if allows_multiple_tenants:
        # Get information for all tenants listed
        for tenant_name in udl2_conf[namespace]:
            create_sqlalchemy(namespace, udl2_conf, allow_schema_create, metadata_generator, tenant_name)
    else:
        create_sqlalchemy(namespace, udl2_conf, allow_schema_create, metadata_generator)


def create_sqlalchemy(namespace, udl2_conf, allow_schema_create, metadata_generator, tenant=None):
    """

    :param namespace:
    :param udl2_conf:
    """
    lookup_tenant = tenant if tenant else DEFAULT_TENANT
    datasource_name = namespace + '.' + lookup_tenant
    db_dict = udl2_conf[namespace]
    db_defaults = udl2_conf['db_defaults']
    tenant_dict = db_dict[lookup_tenant] if tenant else db_dict

    settings = {
        'url': tenant_dict['url'],
        'schema_name': tenant_dict['db_schema'],
        #'max_overflow': db_defaults['max_overflow'],
        'echo': db_defaults['echo'],
        #'pool_size': db_defaults['pool_size']
    }
    setup_db_connection_from_ini(settings, '', metadata_generator, datasource_name, allow_schema_create)
