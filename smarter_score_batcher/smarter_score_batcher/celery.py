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

'''
Created on Jul 29, 2014

@author: tosako
'''
from edworker.celery import setup_celery as setup_for_worker, configure_celeryd,\
    get_config_file
from edcore.database import initialize_db
from smarter_score_batcher.database.tsb_connector import TSBDBConnection


PREFIX = 'smarter_score_batcher.celery'


def setup_celery(settings, prefix=PREFIX, db_connection=True):
    '''
    Setup celery based on parameters defined in setting (ini file).
    This calls by client application when dictionary of settings is given

    :param settings:  dict of configurations
    :param prefix: prefix in configurations used for configuring celery
    '''
    global conf
    conf = settings
    setup_for_worker(celery, settings, prefix)
    if db_connection:
        # This creates the schema if it doesn't exist
        initialize_db(TSBDBConnection, settings, allow_schema_create=True)


# Create an instance of celery, check if it's for prod celeryd mode and configure it for prod mode if so
celery, conf = configure_celeryd(PREFIX, prefix=PREFIX)
prod_config = get_config_file()
if prod_config:
    setup_celery(conf, db_connection=True)
