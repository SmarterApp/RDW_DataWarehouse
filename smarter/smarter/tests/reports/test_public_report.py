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
Created on Oct 21, 2015

@author: dip
'''
import unittest
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.security import Allow
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map_public_reports
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport
from smarter.reports.compare_pop_report import set_default_min_cell_size
from smarter.reports.helpers.constants import Constants
from smarter.reports.public_report import mask_state_code, get_public_comparing_populations_report, mask_breadcrumb, EDWARE_PUBLIC_SECRET
from pyramid.registry import Registry
from smarter.utils.encryption import encode, decode
from edcore.database.routing import PublicDBConnection


SECRET = 'test_secret_1234'


class TestComparingPopulations(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.reg = Registry()
        self.reg.settings = {EDWARE_PUBLIC_SECRET: SECRET}
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived,public.very_shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map_public_reports({get_unittest_tenant_name(): 'NC'})
        set_default_min_cell_size(0)
        # so that it works with unittest edcore module
        PublicDBConnection.CONFIG_NAMESPACE = 'edware.db'

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_mask_state_url(self):
        stateCode = 'AA'  # dummy state code
        sid = 'ABCDEFGHIJK'
        report = {Constants.RECORDS: [{Constants.PARAMS: {Constants.STATECODE: stateCode, Constants.ID: '123456789'}}]}
        report = mask_state_code(report, sid)
        self.assertTrue(Constants.SID in report[Constants.RECORDS][0][Constants.PARAMS])
        self.assertFalse(Constants.STATECODE in report[Constants.RECORDS][0][Constants.PARAMS])
        self.assertEqual(sid, report[Constants.RECORDS][0][Constants.PARAMS][Constants.SID])

    def test_mask_breadcrumb(self):
        sid = 'ABCDEFGHIJK'
        report = {Constants.CONTEXT: {Constants.ITEMS: [{Constants.NAME: 'Test Name', Constants.TYPE: 'state', Constants.STATECODE: 'AA', Constants.ID: 'AA'}]}}
        report = mask_breadcrumb(report, sid)
        #  check id is encoded
        self.assertEqual(sid, report[Constants.CONTEXT][Constants.ITEMS][0][Constants.ID])

    def test_state_view(self):
        testParam = {}
        testParam[Constants.SID] = encode(SECRET, 'NC')
        testParam[Constants.ASMTYEAR] = 2016
        results = get_public_comparing_populations_report(testParam)
        self.assertIsNotNone(results)
        self.assertTrue(results['records'][0]['params']['isPublic'])
        self.assertTrue(results['context']['permissions']['pii']['all'])

if __name__ == "__main__":
    unittest.main()
