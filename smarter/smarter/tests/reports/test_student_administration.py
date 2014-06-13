from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.security import Allow

from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from smarter.reports.student_administration import get_asmt_academic_years,\
    get_student_reg_academic_years
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map


class TestStudentAdministration(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def tearDown(self):
        testing.tearDown()

    def test_get_academic_years(self):
        state_code = 'NC'
        test_cases = [
            # year_back, expect_value
            (-1, [2016]),
            (0, [2016]),
            (1, [2016]),
            (2, [2016, 2015]),
            (5, [2016, 2015]),
        ]
        for year_back, expect in test_cases:
            results = get_asmt_academic_years(state_code, None, year_back)
            self.assertEqual(expect, results, "%d most recent academic year should be %r" % (year_back, expect))

    def test_get_student_reg_academic_years(self):
        results = get_student_reg_academic_years('NC')
        self.assertEqual(0, len(results))
        results = get_student_reg_academic_years('ES')
        self.assertEqual(2, len(results))
        self.assertIn(2015, results)
        self.assertIn(2016, results)
