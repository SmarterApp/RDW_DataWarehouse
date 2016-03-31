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
Created on Jun 24, 2013

@author: dip
'''
import unittest

from zope import component

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name

from edauth.security.session_backend import ISessionBackend, SessionBackend

import services
from services.celery import setup_celery

from smarter.trigger.pre_pdf_generator import prepare_pre_pdf, trigger_pre_pdf


class TestPrePdfGenerator(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.tenant = get_unittest_tenant_name()

    def tearDown(self):
        pass

    def test_prepare_pre_pdf(self):
        results = prepare_pre_pdf(self.tenant, 'NC', '90901b70-ddaa-11e2-a95d-68a86d3c2f82')
        self.assertEqual(822, len(results))

    def test_prepare_pre_pdf_with_future_date(self):
        results = prepare_pre_pdf(self.tenant, 'NC', 'd1d7d814-ddb1-11e2-b3dd-68a86d3c2f82')
        self.assertEqual(0, len(results))

    def test_trigger_pre_pdf_with_empty_results(self):
        triggered = trigger_pre_pdf({}, self.tenant, 'NC', [])
        self.assertFalse(triggered)

    def test_trigger_pre_pdf(self):
        settings = {'pdf.base.url': 'http://dummy:1223',
                    'pdf.batch.job.queue': 'dummy',
                    'pdf.health_check.job.queue': 'dummy',
                    'batch.user.session.timeout': 10000,
                    'auth.policy.secret': 'dummySecret',
                    'auth.policy.cookie_name': 'dummy',
                    'auth.policy.hashalg': 'sha1',
                    'celery.CELERY_ALWAYS_EAGER': True,
                    'pdf.minimum_file_size': 0,
                    'cache.regions': 'public.data, session',
                    'cache.type': 'memory'}
        component.provideUtility(SessionBackend(settings), ISessionBackend)
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        setup_celery(settings, "celery")

        results = [{
            'school_id': '242',
            'district_id': '228',
            'effective_date': '20151213',
            'asmt_type': 'SUMMATIVE',
            'asmt_period_year': '2015',
            'asmt_grade': '3',
            'student_id': '34140997-8949-497e-bbbb-5d72aa7dc9cb'
        }]
        triggered = trigger_pre_pdf(settings, 'NC', self.tenant, results)
        self.assertTrue(triggered)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
