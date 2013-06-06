from edschema.ed_metadata import generate_ed_metadata
from database.generic_connector import setup_db_connection_from_ini
from smarter.database.datasource import get_datasource_name, parse_db_settings, get_db_config_prefix
from database.connector import IDbUtil
from zope.component import getUtilitiesFor


def get_data_source_names():
    ''' Get list of names for existing registered db utils '''
    return [x[0] for x in list(getUtilitiesFor(IDbUtil))]


def initialize_db(settings):
    # setup database connection per tenant
    tenants, db_options = parse_db_settings(settings)
    for tenant in tenants:
        prefix = get_db_config_prefix(tenant)
        schema_key = prefix + 'schema_name'
        metadata = generate_ed_metadata(db_options[schema_key])
        # Pop schema name as sqlalchemy doesn't like db.schema_name being passed
        db_options.pop(schema_key)
        setup_db_connection_from_ini(db_options, prefix, metadata, datasource_name=get_datasource_name(tenant))
