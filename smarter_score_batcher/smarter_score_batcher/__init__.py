# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from pyramid.config import Configurator
import logging
import edauth
import edapi
from smarter_common.security.root_factory import RootFactory, Permission
import os
from smarter_score_batcher.utils import xsd
from smarter_score_batcher.celery import setup_celery as setup_xml_celery, PREFIX as prefix
from edauth import configure
from pyramid_beaker import set_cache_regions_from_settings
from edcore.utils.utils import set_environment_path_variable, \
    get_config_from_ini


logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Configure for environment
    set_environment_path_variable(settings)
    configure(settings)

    config = Configurator(settings=settings, root_factory=RootFactory)

    # Pass edauth the roles/permission mapping
    config.include(edauth)
    edauth.set_roles(RootFactory.__acl__)
    # include add routes from edapi. Calls includeme
    config.include(edapi)
    here = os.path.abspath(os.path.dirname(__file__))
    xsd_file = os.path.join(here, settings['smarter_score_batcher.xsd.path'])
    xsd.xsd = xsd.XSD(xsd_file)

    mode = settings.get('mode', 'prod').upper()
    init_db = False if mode == 'PROD' else True
    # Set up celery. Important - This must happen before scan
    # We don't need to initialize the db in Prod mode as only celery workers needs db connection
    setup_xml_celery(settings, prefix=prefix, db_connection=init_db)

    set_cache_regions_from_settings(get_config_from_ini(settings, 'smarter_score_batcher', True))

    config.add_route('xml', '/services/xml')
    config.add_route('error', '/error')
    config.add_route('heartbeat', '/services/heartbeat')
    config.scan(ignore=['smarter_score_batcher.custom', 'smarter_score_batcher.tests.custom'])

    # Set default permission
    config.set_default_permission(Permission.LOAD)

    logger.info("Smarter tsb started")
    return config.make_wsgi_app()
