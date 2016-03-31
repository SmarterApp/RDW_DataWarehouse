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
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from sqlalchemy.sql.expression import select, and_
from smarter.trigger.pre_cache_generator import update_ed_stats_for_precached
from edcore.database.stats_connector import StatsDBConnection


class Test(Unittest_with_stats_sqlite):

    def testUpdate_ed_stats_for_precached(self):
        update_ed_stats_for_precached('9000')
        with StatsDBConnection() as connector:
            udl_stats = connector.get_table('udl_stats')
            query = select([udl_stats.c.last_pre_cached.label('last_pre_cached'), ],
                           from_obj=[udl_stats])
            query = query.where(and_(udl_stats.c.rec_id == '9000'))
            results = connector.get_result(query)
        self.assertIsNotNone(results[0]['last_pre_cached'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
