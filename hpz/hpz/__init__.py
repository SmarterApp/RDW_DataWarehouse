from pyramid.config import Configurator
import logging
from hpz import frs, swi
from hpz.database.hpz_connector import initialize_db
import edauth
from pyramid_beaker import set_cache_regions_from_settings
from smarter_common.security.root_factory import RootFactory
import os

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    initialize_db(settings)
    prepare_env(settings)

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

    config.scan()

    logger.info("HPZ Started")

    return config.make_wsgi_app()


def prepare_env(settings):
    auth_idp_metadata = settings.get('auth.idp.metadata', None)
    if auth_idp_metadata is not None:
        if auth_idp_metadata.startswith('../'):
            settings['auth.idp.metadata'] = os.path.abspath(os.path.join(os.path.dirname(__file__), auth_idp_metadata))
