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

from edschema.database.tests.utils.unittest_with_sqlite import Unittest_with_sqlite
from smarter_score_batcher.database.tsb_connector import config_namespace,\
    TSBDBConnection
from smarter_score_batcher.database.metadata import generate_tsb_metadata
from smarter_score_batcher.constant import Constants


class Unittest_with_tsb_sqlite(Unittest_with_sqlite):

    @classmethod
    def setUpClass(cls, force_foreign_keys=False):
        super().setUpClass(datasource_name=config_namespace, metadata=generate_tsb_metadata(), use_metadata_from_db=False, resources_dir=None, force_foreign_keys=force_foreign_keys)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def tearDown(self):
        with TSBDBConnection() as conn:
            conn.execute(conn.get_table(Constants.TSB_ASMT).delete())
            conn.execute(conn.get_table(Constants.TSB_METADATA).delete())
            conn.execute(conn.get_table(Constants.TSB_ERROR).delete())
