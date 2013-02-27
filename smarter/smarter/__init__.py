from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.path import caller_package, caller_module, package_of
import edauth
import edapi
import os
from edschema.ed_metadata import generate_ed_metadata
import pyramid
from zope import component
from database.connector import DbUtil, IDbUtil
import logging
from smarter.security.root_factory import RootFactory
import platform
import ctypes
import subprocess


logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Prepare for environment specific
    prepare_env(settings)
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

    config.add_static_view('assets', '../assets', cache_max_age=0, permission='view')

    # scans smarter
    config.scan()

    # Set default permission on all views
    config.set_default_permission('view')

    logger.info("Smarter started")

    return config.make_wsgi_app()


def prepare_env(settings):
    mode = settings.get('mode', 'prod').upper()
    if mode == 'DEV':
        here = os.path.abspath(os.path.dirname(__file__))
        assets_dir = os.path.abspath(here + '/../assets')
        parent_assets_dir = os.path.abspath(here + '/../../assets')
        css_dir = os.path.join(parent_assets_dir, "css")
        less_dir = os.path.join(parent_assets_dir, "less")
        # We're assuming we only have one less file to compile
        less_file = os.path.join(less_dir, 'style.less')
        css_file = os.path.join(css_dir, 'style.css')

        # delete all css file before lessc generates css files from less files
        css_filelist = [f for f in os.listdir(css_dir) if f.endswith('.css')]
        for f in css_filelist:
            target_file = os.path.join(css_dir, f)
            if os.access(target_file, os.W_OK):
                os.unlink(target_file)

        command_opts = ['lessc', '-x', less_file, css_file]
        if platform.system() == 'Windows':
            # Create a sym link
            if not os.path.lexists(assets_dir):
                kernel_dll = ctypes.windll.LoadLibrary("kernel32.dll")
                # TODO check error for failures
                kernel_dll.CreateSymbolicLink(parent_assets_dir, assets_dir, 1)
            command_opts.insert(0, 'node')
        else:
            if not os.path.lexists(assets_dir):
                os.symlink(parent_assets_dir, assets_dir)

        if os.access(less_dir, os.W_OK):
            rtn_code = subprocess.call(command_opts)
            if rtn_code != 0:
                pass
                # Failed
    else:
        auth_idp_metadata = settings.get('auth.idp.metadata', None)
        if auth_idp_metadata is not None:
            if auth_idp_metadata.startswith('../'):
                settings['auth.idp.metadata'] = os.path.abspath(os.path.join(os.path.dirname(__file__), auth_idp_metadata))
