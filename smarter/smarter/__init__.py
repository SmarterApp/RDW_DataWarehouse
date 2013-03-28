from pyramid.config import Configurator
import edauth
import edapi
import os
import pyramid
import logging
from smarter.security.root_factory import RootFactory
import platform
import subprocess
from database.generic_connector import setup_db_connection_from_ini
from edschema.ed_metadata import generate_ed_metadata
import atexit
import signal

logger = logging.getLogger(__name__)
CAKE_PROC = None


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Prepare for environment specific
    if 'smarter.PATH' in settings:
        os.environ['PATH'] += os.pathsep + settings['smarter.PATH']
    prepare_env(settings)
    config = Configurator(settings=settings, root_factory=RootFactory)

    #set_cache_regions_from_settings(settings)
    # include beaker for caching
    config.include('pyramid_beaker')

    # setup database connection
    metadata = generate_ed_metadata(settings['edware.schema_name'])
    setup_db_connection_from_ini(settings, 'edware', metadata, datasource_name='smarter')

    # include edauth. Calls includeme
    config.include(edauth)
    # Pass edauth the roles/permission mapping that is defined in smarter
    edauth.set_roles(RootFactory.__acl__)

    # include add routes from edapi. Calls includeme
    config.include(edapi)

    static_max_age = int(settings.get('smarter.resources.static.max_age', 3600))
    config.add_static_view('assets/css', '../assets/css', cache_max_age=static_max_age)
    config.add_static_view('assets/data', '../assets/data', cache_max_age=static_max_age)
    config.add_static_view('assets/images', '../assets/images', cache_max_age=static_max_age)
    config.add_static_view('assets/js', '../assets/js', cache_max_age=static_max_age)
    config.add_static_view('assets/test', '../assets/test', cache_max_age=static_max_age)

    config.add_static_view('assets/html', '../assets/html', cache_max_age=static_max_age, permission='view')

    # scans smarter
    config.scan()

    # Set default permission on all views
    config.set_default_permission('view')

    logger.info("Smarter started")

    return config.make_wsgi_app()


def prepare_env(settings):
    '''
    Prepare environment for assets, less, compile coffeescripts
    '''
    global CAKE_PROC
    mode = settings.get('mode', 'prod').upper()
    if mode == 'DEV':
        here = os.path.abspath(os.path.dirname(__file__))
        assets_dir = os.path.abspath(os.path.join(os.path.join(here, '..'), 'assets'))
        parent_assets_dir = os.path.abspath(os.path.join(os.path.join(os.path.join(here, '..'), '..'), 'assets'))
        css_dir = os.path.join(parent_assets_dir, "css")
        less_dir = os.path.join(parent_assets_dir, "less")

        # delete all css file before lessc generates css files from less files
        css_filelist = [f for f in os.listdir(css_dir) if f.endswith('.css')]
        for f in css_filelist:
            target_file = os.path.join(css_dir, f)
            if os.access(target_file, os.W_OK):
                os.unlink(target_file)

        shell = False

        # For windows env, set shell to true
        if platform.system() == 'Windows':
            shell = True

        # Create a symlink if it doesn't exist
        if not os.path.lexists(assets_dir):
            os.symlink(parent_assets_dir, assets_dir, target_is_directory=True)

        # Run cake watch - builds and watches
        if os.access(less_dir, os.W_OK):
            try:
                current_dir = os.getcwd()
                os.chdir(assets_dir)
                if settings.get('run.npm.update', 'false').lower() == 'true':
                    # Run npm update
                    command_opts = ['npm', 'update']
                    rtn_code = subprocess.call(command_opts, shell=shell)
                    if rtn_code != 0:
                        logger.warning('npm install command failed')
                # Run cake
                command_opts = ['cake', 'watch']
                CAKE_PROC = subprocess.Popen(command_opts, shell=shell)
            except:
                logger.warning('cake command failed')
            finally:
                # Change the directory back to original
                os.chdir(current_dir)
        # catch the kill signal
        signal.signal(signal.SIGTERM, handler)

    auth_idp_metadata = settings.get('auth.idp.metadata', None)
    if auth_idp_metadata is not None:
        if auth_idp_metadata.startswith('../'):
            settings['auth.idp.metadata'] = os.path.abspath(os.path.join(os.path.dirname(__file__), auth_idp_metadata))


@atexit.register
def shutdown():
    '''
    Called when pyramid shuts down
    '''
    logger.info("Smarter is shuting down.")
    # CAKE_PROC is only assigned in dev mode, we kill the process that started 'cake watch'
    if CAKE_PROC:
        logger.info("Killing cake process - pid " + str(CAKE_PROC.pid))
        CAKE_PROC.kill()


def handler():
    '''
    Handles SIGTERM
    '''
    logger.log("SIGTERM called")
