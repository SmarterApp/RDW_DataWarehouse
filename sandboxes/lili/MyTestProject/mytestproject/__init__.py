from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('datatojson1', '/datatojson1')
    config.add_route('datatojson2', '/datatojson2')
    config.add_route('inputdata2','/inputdata2')

    config.scan()
    return config.make_wsgi_app()