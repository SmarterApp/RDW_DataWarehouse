from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.path import caller_package, caller_module, package_of
import sys
import edapi
import os
from edschema.ed_metadata import generate_ed_metadata
import pyramid
from zope import component
from database.connector import DbUtil, IDbUtil
from lesscss import LessCSS
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'smarter.PATH' in settings:
        os.environ['PATH'] += os.pathsep + settings['smarter.PATH']
    # TODO: Spike, pool_size, max_overflow, timeout

    config = Configurator(settings=settings)

    # zope registration
    engine = engine_from_config(settings, "sqlalchemy.", pool_size=20, max_overflow=10)
    metadata = generate_ed_metadata(settings['edschema.schema_name'])
    dbUtil = DbUtil(engine=engine, metadata=metadata)
    component.provideUtility(dbUtil, IDbUtil)

    # include add routes from edapi. Calls includeme
    config.include(edapi)

    # TODO symbolic link should be done in development mode only
    here = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.abspath(here + '/../assets')
    parent_assets_dir = os.path.abspath(here + '/../../assets')
    try:
        if not os.path.lexists(assets_dir):
            os.symlink(parent_assets_dir, assets_dir)
    except PermissionError:
        pass

    LessCSS(media_dir=parent_assets_dir + "/less", output_dir=parent_assets_dir + "/css", based=False)

    config.add_static_view('assets', '../assets', cache_max_age=0, permission='view')

    # scans smarter
    config.scan()

    return config.make_wsgi_app()
