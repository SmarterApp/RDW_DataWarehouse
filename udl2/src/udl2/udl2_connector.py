__author__ = 'swimberly'

from database.connector import DBConnection
from udl2.database import generate_udl2_metadata
from database.generic_connector import setup_db_connection_from_ini


CONF_NAMESPACE = 'udl2_db'


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
        return CONF_NAMESPACE

    @staticmethod
    def get_datasource_name(**kwargs):
        '''
        Returns datasource name for UDL Stats
        '''
        return CONF_NAMESPACE

    @staticmethod
    def generate_metadata(schema_name=None, bind=None):
        """
        Generate Metadata for UDL
        """
        return generate_udl2_metadata(schema_name=schema_name, bind=bind)


def initialize_db(connector_cls, udl2_conf, allow_schema_create=False):
    """
    Setup connection for udl2
    :param connector_cls:
    :param udl2_conf:
    :param allow_schema_create:
    :return:
    """
    # will need to update if multiple tenants exist for udl2
    schema = udl2_conf['udl2_db']['db_schema']
    metadata = connector_cls.generate_metadata(schema)
    settings = create_sqlalchemy_settings_from_conf(connector_cls, udl2_conf)
    setup_db_connection_from_ini(settings, '', metadata, connector_cls.get_datasource_name(), allow_schema_create)


def create_sqlalchemy_settings_from_conf(connector_cls, udl2_conf):
    """

    :param connector_cls
    :param udl2_conf:
    :return:
    """
    db_dict = udl2_conf[connector_cls.get_namespace()]
    db_url = '{db_driver}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    db_url = db_url.format(db_driver=db_dict['db_driver'], db_user=db_dict['db_user'], db_password=db_dict['db_pass'],
                           db_host=db_dict['db_host'], db_port=db_dict['db_port'], db_name=db_dict['db_name'])
    settings = {
        'url': db_url,
        'max_overflow': db_dict['max_overflow'],
        'echo': db_dict['echo'],
        'pool_size': db_dict['pool_size'],
    }
    return settings