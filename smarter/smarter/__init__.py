import os
import logging
import platform
import subprocess
import atexit
import signal
import sys

from pyramid.config import Configurator
import pyramid
from pyramid_beaker import set_cache_regions_from_settings

import edauth
import edapi
from smarter_common.security.root_factory import RootFactory
from smarter import services, trigger
from smarter.utils.remote_config import get_remote_config
from edcore.database import initialize_db
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.database.stats_connector import StatsDBConnection
from services.celery import setup_celery as setup_services_celery, PREFIX as servicesPrefix
from edextract.celery import setup_celery as setup_extract_celery, PREFIX as edextractPrefix
from edcore.security.tenant import set_tenant_map
from smarter.reports.student_administration import set_default_year_back
from hpz_client.frs.config import initialize as initialize_hpz


logger = logging.getLogger(__name__)
CAKE_PROC = None


def main(global_config, **settings):
    """
    Starting point for the Smarter application. Prepares the environment and
    applies configurations. Sets paths, permissions, routes. Calls includeme
    methods of EdAuth, EdApi, and EdServices.

    Returns a Pyramid WSGI application.
    """
    mode = settings.get('mode', 'prod').upper()

    # read remote config
    if mode == 'PROD' and 'edware.remote_config.url' in settings:
        url = settings['edware.remote_config.url']
        settings = get_remote_config(url)

    # Prepare for environment specific
    if 'smarter.PATH' in settings:
        os.environ['PATH'] += os.pathsep + settings['smarter.PATH']
    prepare_env(settings)

    # set beaker cache region
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings, root_factory=RootFactory)

    tenant_mapping = initialize_db(EdCoreDBConnection, settings)
    initialize_db(StatsDBConnection, settings, allow_schema_create=True)

    # save tenancy mapping
    set_tenant_map(tenant_mapping)

    year_back = settings['smarter.reports.year_back']
    set_default_year_back(year_back)

    # setup celery
    setup_services_celery(settings, prefix=servicesPrefix)
    setup_extract_celery(settings, prefix=edextractPrefix)

    initialize_hpz(settings)

    # include edauth. Calls includeme
    config.include(edauth)
    # Pass edauth the roles/permission mapping that is defined in smarter
    edauth.set_roles(RootFactory.__acl__)

    # include add routes from edapi. Calls includeme
    config.include(edapi)

    # Get absolute paths
    here = os.path.abspath(os.path.dirname(__file__))
    assets_dir = os.path.abspath(os.path.join(os.path.join(here, '..'), 'assets'))

    static_max_age = int(settings.get('smarter.resources.static.max_age', 3600))
    config.add_static_view('assets/css', os.path.join(assets_dir, 'css'), cache_max_age=static_max_age)
    config.add_static_view('assets/data', os.path.join(assets_dir, 'data'), cache_max_age=static_max_age)
    config.add_static_view('assets/images', os.path.join(assets_dir, 'images'), cache_max_age=static_max_age)
    config.add_static_view('assets/js', os.path.join(assets_dir, 'js'), cache_max_age=static_max_age)
    config.add_static_view('assets/html', os.path.join(assets_dir, 'html'), cache_max_age=static_max_age)
    config.add_static_view('assets/public', os.path.join(assets_dir, 'public'), cache_max_age=static_max_age, permission=pyramid.security.NO_PERMISSION_REQUIRED)

    # Only expose test in non-production modes
    if mode != 'PROD':
        config.add_static_view('assets/test', os.path.join(assets_dir, 'test'), cache_max_age=static_max_age)

    disable_stack_trace = settings.get('disable_stack_trace', 'False').upper()
    if disable_stack_trace == 'TRUE':
        # we would like to disable the stack trace when we are in production mode
        sys.tracebacklimit = 0

    # route for error
    config.add_route('error', '/assets/public/error.html')

    # include add routes from smarter.services. Calls includeme
    config.include(services)

    # include add routes from smarter.trigger. Calls includeme
    config.include(trigger)

    # scans smarter
    config.scan()

    # Set default permission on all views
    config.set_default_permission('view')

    logger.info("Smarter started")

    return config.make_wsgi_app()


def prepare_env(settings):
    '''
    Prepare environment for assets, LESS. Compile coffeescript.
    '''
    global CAKE_PROC
    mode = settings.get('mode', 'prod').upper()
    if mode == 'DEV':
        here = os.path.abspath(os.path.dirname(__file__))
        smarter_dir = os.path.abspath(os.path.join(here, '..'))
        assets_dir = os.path.abspath(os.path.join(os.path.join(os.path.join(here, '..'), '..'), 'assets'))

        shell = False
        # For windows env, set shell to true
        if platform.system() == 'Windows':
            shell = True

        # Run cake setup and watch
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
            command_opts = ['node_modules/coffee-script/bin/cake', '-m', 'DEV', '-w', 'TRUE', '-a', assets_dir, '-s', smarter_dir, 'setup']
            CAKE_PROC = subprocess.Popen(command_opts, shell=shell)
        except:
            logger.warning('cake command failed')
        finally:
            # Change the directory back to original
            os.chdir(current_dir)
        # catch the kill signal
        signal.signal(signal.SIGTERM, sig_term_handler)

    auth_idp_metadata = settings.get('auth.idp.metadata', None)
    if auth_idp_metadata is not None:
        if auth_idp_metadata.startswith('../'):
            settings['auth.idp.metadata'] = os.path.abspath(os.path.join(os.path.dirname(__file__), auth_idp_metadata))


@atexit.register
def shutdown():
    '''
    Called when pyramid shuts down
    '''
    logger.info("Smarter is shutting down.")
    # CAKE_PROC is only assigned in dev mode, we kill the process that started 'cake watch'
    if CAKE_PROC:
        logger.info("Killing cake process - pid " + str(CAKE_PROC.pid))
        CAKE_PROC.kill()


def sig_term_handler():
    '''
    Handles SIGTERM
    '''
    logger.log("SIGTERM called")
