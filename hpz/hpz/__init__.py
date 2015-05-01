from pyramid.config import Configurator
import logging
from hpz import frs, swi, services
from hpz.database.hpz_connector import initialize_db
import edauth
from pyramid_beaker import set_cache_regions_from_settings
from smarter_common.security.root_factory import RootFactory
import os
from edauth import configure
from edcore.utils.utils import read_ini, get_config_from_ini, run_cron_job
from hpz.utils.maintenance import cleanup
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

HPZ_EXPIRATION = 'hpz.record_expiration'
HPZ_INI_PATH = "/opt/edware/conf/hpz.ini"

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    initialize_db(settings)
    configure(settings)

    # set beaker cache region
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings, root_factory=RootFactory)

    # include edauth. Calls includeme
    config.include(edauth)
    # Pass edauth the roles/permission mapping that is defined in hpz
    edauth.set_roles(RootFactory.__acl__)

    # include add routes from frs. Calls includeme
    config.include(frs)
    config.include(swi)
    config.include(services)

    config.scan()

    #Clean up old files from HPZ
    hpz_config = ConfigParser()
    hpz_config.read(HPZ_INI_PATH)
    settings = hpz_config['app:main']
    run_cron_job(settings, HPZ_EXPIRATION + '.', cleanup)

    logger.info("HPZ Started")

    return config.make_wsgi_app()
