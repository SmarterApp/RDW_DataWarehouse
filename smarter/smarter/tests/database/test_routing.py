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
Created on Oct 22, 2015

@author: dip
'''
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite_no_data_load,\
    get_unittest_tenant_name
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.security.tenant import set_tenant_map
from edcore.database.routing import PublicDBConnection, ReportingDbConnection


class TestRouting(Unittest_with_edcore_sqlite_no_data_load):
    def setUp(self):
        set_tenant_map({get_unittest_tenant_name(): 'NC'})

    def tearDown(self):
        PublicDBConnection.CONFIG_NAMESPACE = 'edware.public.db'

    def test_protected_connection(self):
        with ReportingDbConnection(tenant=get_unittest_tenant_name(), state_code='NC', is_public=False) as instance:
            self.assertIsInstance(instance, EdCoreDBConnection)

    def test_public_connection(self):
        PublicDBConnection.CONFIG_NAMESPACE = 'edware.db'
        with ReportingDbConnection(tenant=get_unittest_tenant_name(), state_code='NC', is_public=True) as instance:
            self.assertIsInstance(instance, PublicDBConnection)
