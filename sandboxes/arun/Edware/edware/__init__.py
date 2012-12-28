from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('checkstatus','/status')    
    config.add_route( 'generateComparePopulations','/comPopResults')
    config.add_route( 'inputComparePopulations','/comPop')
    config.scan()
    return config.make_wsgi_app()
