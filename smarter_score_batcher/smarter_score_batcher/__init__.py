from pyramid.config import Configurator
import logging
import edauth
import edapi
from smarter_common.security.root_factory import RootFactory
import os
from smarter_score_batcher.utils import xsd
from smarter_score_batcher.celery import setup_celery as setup_xml_celery, PREFIX as prefix
from smarter_score_batcher import trigger
from edauth import configure


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

    config.add_route('xml', '/services/xml')
    config.add_route('error', '/error')
    config.scan()

    # Set default permission
    config.set_default_permission('load')
    
    # Configure for environment
    configure(settings)
    if 'smarter_score_batcher.PATH' in settings:
        os.environ['PATH'] += os.pathsep + settings['smarter_score_batcher.PATH']

    logger.info("Smarter tsb started")
    return config.make_wsgi_app()
