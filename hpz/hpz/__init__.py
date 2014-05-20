from pyramid.config import Configurator
import logging
from hpz import frs
from hpz.database.hpz_connector import initialize_db

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    initialize_db(settings)

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # include add routes from frs. Calls includeme
    config.include(frs)

    # Adding a dummy route for download endpoint
    config.add_route('download', '/{reg_id}')
    config.scan()

    logger.info("HPZ Started")

    return config.make_wsgi_app()
