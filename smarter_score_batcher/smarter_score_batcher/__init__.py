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
    # Pass edauth the roles/permission mapping that is defined in smarter
    edauth.set_roles(RootFactory.__acl__)
    # include add routes from edapi. Calls includeme
    config.include(edapi)

    config.add_route('xml', '/services/xml')
    config.scan()
    # Set default permission on all views
    config.set_default_permission('view')

    logger.info("Smarter tsb started")
    return config.make_wsgi_app()
