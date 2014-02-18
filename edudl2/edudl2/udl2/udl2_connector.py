from edudl2.udl2.database import generate_udl2_metadata
__author__ = 'swimberly'

from database.connector import DBConnection
from database.generic_connector import setup_db_connection_from_ini
from edschema.metadata_generator import generate_ed_metadata


UDL_NAMESPACE = 'udl2_db_conn'
TARGET_NAMESPACE = 'target_db_conn'
PRODUCTION_NAMESPACE = 'production_db_conn'


class UDL2DBConnection(DBConnection):
    """
    DBConnector for the UDL Database
    """
    def __init__(self, tenant=None):
        name = UDL2DBConnection.get_datasource_name()
        if tenant:
            name += '.' + tenant
        super().__init__(name=name)

    @staticmethod
    def get_namespace():
        return UDL_NAMESPACE

    @staticmethod
    def get_datasource_name(**kwargs):
        '''
        Returns datasource name for UDL Stats
        '''
        return UDL_NAMESPACE

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        """
        Generate Metadata for UDL
        """
        return generate_udl2_metadata(schema_name=schema_name, bind=bind)

    @staticmethod
    def allows_multiple_tenants():
        """
        Does this connection class support multiple tenants
        """
        return False


class TargetDBConnection(DBConnection):
    """
    DBConnector for UDL Target Database
    """
    def __init__(self, tenant='edware'):
        name = TargetDBConnection.get_datasource_name(tenant)
        super().__init__(name=name)

    @staticmethod
    def get_namespace():
        return TARGET_NAMESPACE

    @staticmethod
    def get_datasource_name(tenant="edware"):
        """
        Returns datasource name for UDL Stats
        """
        return TARGET_NAMESPACE + '.' + tenant

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        """
        Generate Metadata for Target
        """
        return generate_ed_metadata(schema_name=schema_name, bind=bind)

    @staticmethod
    def allows_multiple_tenants():
        """
        Does this connection class support multiple tenants
        """
        return True


class ProductionDBConnection(DBConnection):
    """
    DBConnector for Edware Production Database
    """
    def __init__(self, tenant='edware'):
        name = ProductionDBConnection.get_datasource_name(tenant)
        super().__init__(name=name)

    @staticmethod
    def get_namespace():
        return PRO_NAMESPACE

    @staticmethod
    def get_datasource_name(tenant="edware"):
        """
        Returns datasource name for Production table
        """
        return TARGET_NAMESPACE + '.' + tenant

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        """
        Generate Metadata for Target
        """
        return generate_ed_metadata(schema_name=schema_name, bind=bind)

    @staticmethod
    def allows_multiple_tenants():
        """
        Does this connection class support multiple tenants
        """
        return True


def initialize_db(connector_cls, udl2_conf, allow_schema_create=False):
    """
    Setup connection for udl2
    :param connector_cls:
    :param udl2_conf:
    :param allow_schema_create:
    :return:
    """
    # will need to update if multiple tenants exist for udl2
    #schema = udl2_conf['udl2_db']['db_schema']
    tenants = {}

    if connector_cls.allows_multiple_tenants():
        # Get information for all tenants listed
        for tenant_name in udl2_conf[connector_cls.get_namespace()]:
            tenants[tenant_name] = create_sqlalchemy_settings_from_conf(connector_cls, udl2_conf, tenant_name)

        # add default tenant information to dict (this should already be listed)
        default_tenant = udl2_conf['multi_tenant']['default_tenant']
        tenants[default_tenant] = create_sqlalchemy_settings_from_conf(connector_cls, udl2_conf, default_tenant)

    if tenants:
        for tenant in tenants:
            settings, schema = tenants[tenant]
            metadata = connector_cls.generate_metadata(schema)
            setup_db_connection_from_ini(settings, '', metadata, connector_cls.get_datasource_name(tenant), allow_schema_create)

    else:
        settings, schema = create_sqlalchemy_settings_from_conf(connector_cls, udl2_conf)
        metadata = connector_cls.generate_metadata(schema)
        setup_db_connection_from_ini(settings, '', metadata, connector_cls.get_datasource_name(), allow_schema_create)


def create_sqlalchemy_settings_from_conf(connector_cls, udl2_conf, tenant=None):
    """

    :param connector_cls:
    :param udl2_conf:
    :return: A tuple contain (settings_dict, schema_name)
    """
    namespace = connector_cls.get_datasource_name(tenant=tenant)
    db_dict = udl2_conf[namespace.split('.')[0]]
    if tenant:
        tenant_dict = db_dict[namespace.split('.')[1]]
    else:
        tenant_dict = db_dict

    schema_name = tenant_dict['db_schema']

    settings = {
        'url': tenant_dict['url'],
        'max_overflow': tenant_dict['max_overflow'],
        'echo': tenant_dict['echo'],
        'pool_size': tenant_dict['pool_size'],
    }
    return settings, schema_name
