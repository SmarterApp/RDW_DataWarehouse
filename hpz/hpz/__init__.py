from pyramid.config import Configurator
import logging
from hpz import frs
from hpz.frs.registration_service import set_base_url
from hpz.database.hpz_connector import initialize_db

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    base_url = settings['base.url']
    set_base_url(base_url)

    initialize_db(settings)

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # include add routes from frs. Calls includeme
    config.include(frs)
    config.scan()

    logger.info("HPZ Started")

    return config.make_wsgi_app()
