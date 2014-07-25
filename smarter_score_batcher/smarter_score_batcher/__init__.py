from pyramid.config import Configurator
import edauth
import edapi
import logging
from smarter_common.security.root_factory import RootFactory

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=RootFactory)
    # include edauth. Calls includeme
    config.include(edauth)
    # include add routes from edapi. Calls includeme
    config.include(edapi)
    # Pass edauth the roles/permission mapping that is defined in smarter
    edauth.set_roles(RootFactory.__acl__)

    config.add_route('xml_catcher', 'services/test/report')
    config.scan()
    logger.info("Smarter tsb started")
    return config.make_wsgi_app()
