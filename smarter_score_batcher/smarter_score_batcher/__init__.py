from pyramid.config import Configurator
import logging
import edauth
import edapi
from smarter_common.security.root_factory import RootFactory, Permission
import os
from smarter_score_batcher.utils import xsd
from smarter_score_batcher.celery import setup_celery as setup_xml_celery, PREFIX as prefix
from smarter_score_batcher import trigger
from edauth import configure
from pyramid_beaker import set_cache_regions_from_settings
from beaker.cache import CacheManager
from edcore.utils.utils import set_environment_path_variable


logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)
    # Pass edauth the roles/permission mapping
    config.include(edauth)
    edauth.set_roles(RootFactory.__acl__)
    # include add routes from edapi. Calls includeme
    config.include(edapi)
    here = os.path.abspath(os.path.dirname(__file__))
    xsd_file = os.path.join(here, settings['smarter_score_batcher.xsd.path'])
    xsd.xsd = xsd.XSD(xsd_file)

    # Set up celery. Important - This must happen before scan
    setup_xml_celery(settings, prefix=prefix)

    set_cache_regions_from_settings(get_sub_settings_by_prefix(settings, 'smarter_score_batcher', True))

    config.add_route('xml', '/services/xml')
    config.add_route('error', '/error')
    config.scan()

    # Set default permission
    config.set_default_permission(Permission.LOAD)

    # Configure for environment
    set_environment_path_variable(settings)
    configure(settings)

    logger.info("Smarter tsb started")
    return config.make_wsgi_app()


def get_sub_settings_by_prefix(settings, prefix, delete_prefix=False):
    return {k[len(prefix) + 1:] if delete_prefix else k: v for (k, v) in settings.items() if k.startswith(prefix)}
