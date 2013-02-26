from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.path import caller_package, caller_module, package_of
import sys
import edauth
import edapi
import os
from edschema.ed_metadata import generate_ed_metadata
import pyramid
from zope import component
from database.connector import DbUtil, IDbUtil
from lesscss import LessCSS
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
import logging
from smarter.security.root_factory import RootFactory

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'smarter.PATH' in settings:
        os.environ['PATH'] += os.pathsep + settings['smarter.PATH']

    config = Configurator(settings=settings)

    engine = engine_from_config(settings, "edware.db.main.")
    metadata = generate_ed_metadata(settings['edschema.schema_name'])

    # zope registration
    dbUtil = DbUtil(engine=engine, metadata=metadata)
    component.provideUtility(dbUtil, IDbUtil)

    # set role-permission mapping
    config.set_root_factory('smarter.security.root_factory.RootFactory')

    # include edauth. Calls includeme
    config.include(edauth)
    edauth.set_roles(RootFactory.__acl__)

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

    # LessCSS has a bug and this is workaround solution.
    # delete all css file before lessc generates css files from less files
    css_dir = os.path.join(parent_assets_dir, "css")
    less_dir = os.path.join(parent_assets_dir, "less")
    css_filelist = [f for f in os.listdir(css_dir) if f.endswith('.css')]
    for f in css_filelist:
        target_file = os.path.join(css_dir, f)
        if os.access(target_file, os.W_OK):
            os.unlink(target_file)
    if os.access(less_dir, os.W_OK):
        LessCSS(media_dir=less_dir, output_dir=css_dir, based=False)

    config.add_static_view('assets', '../assets', cache_max_age=0, permission='view')

    # scans smarter
    config.scan()

    # Set default permission on all views
    config.set_default_permission('view')

    logger.info("Smarter started")

    return config.make_wsgi_app()
