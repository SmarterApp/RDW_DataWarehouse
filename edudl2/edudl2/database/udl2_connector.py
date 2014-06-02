from edudl2.database.metadata.udl2_metadata import generate_udl2_metadata
from edschema.database.connector import DBConnection
from edschema.database.generic_connector import setup_db_connection_from_ini
from sqlalchemy.sql.expression import text
from sqlalchemy.schema import Sequence, CreateSequence
import edcore.database as edcoredb
from edschema.metadata_generator import generate_ed_metadata
from edcore.database.stats_connector import StatsDBConnection
from celery.utils.log import get_task_logger
from sqlalchemy.exc import IntegrityError
from edudl2.udl2_util.database_util import sequence_exists
from edudl2.udl2.constants import Constants

UDL_NAMESPACE = 'udl2_db_conn'
TARGET_NAMESPACE = 'target_db_conn'
PRODUCTION_NAMESPACE = 'prod_db_conn'
DEFAULT_TENANT = 'edware'

logger = get_task_logger(__name__)


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


def initialize_all_db(udl2_conf, udl2_flat_conf):
    # init db engine
    initialize_db_prod(udl2_conf)
    initialize_db_target(udl2_conf)
    initialize_db_udl(udl2_conf)
    # using edcore connection class to init statsdb connection
    # this needs a flat config file rather than udl2 which needs nested config
    edcoredb.initialize_db(StatsDBConnection, udl2_flat_conf, allow_schema_create=True)


def init_udl_tenant_sequences(udl2_conf):
    # Create and sync sequence for each tenant on udl database if it doesn't exist
    with get_udl_connection() as udl_conn:
        all_tenants = udl2_conf.get(PRODUCTION_NAMESPACE)
        udl_schema_name = udl2_conf.get(UDL_NAMESPACE).get(Constants.DB_SCHEMA)
        all_tenant_sequences = {}
        for tenant in all_tenants:
            tenant_seq_name = Constants.TENANT_SEQUENCE_NAME(tenant)
            tenant_schema_name = all_tenants.get(tenant).get(Constants.DB_SCHEMA)
            key = all_tenants.get(tenant).get(Constants.URL) + ':' + tenant_schema_name
            if not key in all_tenant_sequences:
                with get_prod_connection(tenant) as prod_conn:
                    prod_seq_result = prod_conn.execute(text("select nextval(\'{schema_name}.{seq_name} \')".
                                                             format(schema_name=tenant_schema_name,
                                                                    seq_name=Constants.SEQUENCE_NAME)))
                    all_tenant_sequences[key] = prod_seq_result.fetchone()[0]

            if not sequence_exists(udl_conn, tenant_seq_name):
                udl_conn.execute(CreateSequence(Sequence(name=tenant_seq_name, increment=1)))
            udl_conn.execute(text("select setval(\'{schema_name}.{seq_name} \', {value}, {called})".
                                  format(schema_name=udl_schema_name, seq_name=tenant_seq_name,
                                         value=all_tenant_sequences[key], called=True)))


def initialize_db_udl(udl2_conf, allow_create_schema=False):
    initialize_db(UDL_NAMESPACE, generate_udl2_metadata, False, udl2_conf, allow_create_schema)
    # if in init mode
    if allow_create_schema:
        init_udl_tenant_sequences(udl2_conf)


def initialize_db_target(udl2_conf):
    initialize_db(TARGET_NAMESPACE, generate_ed_metadata, True, udl2_conf)
    # Install dblink extension on preprod database if it doesn't exist
    for tenant in udl2_conf.get(TARGET_NAMESPACE):
        with get_target_connection(tenant) as conn:
            try:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public"))
            except IntegrityError as e:
                logger.warning('dblink did not exist at creation time, but fails with IntegrityError')


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
        for tenant_name in udl2_conf.get(namespace):
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
    db_defaults = udl2_conf.get('db_defaults')
    tenant_dict = db_dict[lookup_tenant] if tenant else db_dict

    settings = {
        'url': tenant_dict.get('url'),
        'schema_name': tenant_dict.get('db_schema'),
        'max_overflow': db_defaults.get('max_overflow'),
        'echo': db_defaults.get('echo'),
        'pool_size': db_defaults.get('pool_size')
    }
    setup_db_connection_from_ini(settings, '', metadata_generator, datasource_name, allow_schema_create)
