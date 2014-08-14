from pyramid.config import Configurator
import logging
import edauth
import edapi
from smarter_common.security.root_factory import RootFactory
import os
from smarter_score_batcher.utils import xsd
from smarter_score_batcher.celery import setup_celery as setup_xml_celery, PREFIX as prefix


logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)
    # include edauth. Calls includeme
    config.include(edauth.idp_initiated_includeme)
    # Pass edauth the roles/permission mapping that is defined in smarter
    # edauth.set_roles(RootFactory.__acl__)
    # include add routes from edapi. Calls includeme
    config.include(edapi)
    here = os.path.abspath(os.path.dirname(__file__))
    xsd_file = os.path.join(here, settings['smarter_score_batcher.xsd.path'])
    xsd.xsd = xsd.XSD(xsd_file)

    config.add_route('xml', '/services/xml')
    config.scan()
    # Set default permission on all views
    # config.set_default_permission('view')

    setup_xml_celery(settings, prefix=prefix)

    logger.info("Smarter tsb started")
    return config.make_wsgi_app()
