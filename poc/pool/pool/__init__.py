from pyramid.config import Configurator
import os
import pyramid
import logging
import platform
from sqlalchemy.engine import engine_from_config
from zope import component
from pool.db_util import IEngine, Engine


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Prepare for environment specific

    config = Configurator(settings=settings)

    '''
    Setup a generic db connection
    '''
    sqlengine = engine_from_config(settings, 'edware.db.main.')

    _engine = Engine(engine=sqlengine)

    component.provideUtility(_engine, IEngine)

    # scans smarter
    config.scan()

    config.add_route('test', '/test')

    return config.make_wsgi_app()

#from pyramid.config import Configurator
#from pyramid.response import Response
#from sqlalchemy.engine import engine_from_config
#from pool.db_util import Engine, IEngine
#from zope import component


#def hello_world(request):
#    return Response('Hello %(name)s!' % request.matchdict)

#
#def main(global_config, **settings):
#    config = Configurator(settings)
#    print(config)
#    pass

#if __name__ == '__main__':
#    config = Configurator()
#
#    '''
#    Setup a generic db connection
#    '''
#    sqlengine = engine_from_config("pool.ini", 'test.db.main.')
#
#    _engine = Engine(engine=sqlengine)
#
#    component.provideUtility(_engine, IEngine)
#
#    # scans smarter
#    config.scan()
#    config.add_route('hello', '/hello/{name}')
#    config.add_view(hello_world, route_name='hello')
#    app = config.make_wsgi_app()
#    server = make_server('0.0.0.0', 8080, app)
#    server.serve_forever()
