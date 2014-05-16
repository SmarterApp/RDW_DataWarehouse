from pyramid.config import Configurator
import logging

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('registration', '/registration')
    config.scan()

    logger.info("HPZ Started")

    return config.make_wsgi_app()
