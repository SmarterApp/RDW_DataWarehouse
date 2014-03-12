import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edauth.security.user import RoleRelation
from smarter.reports import student_administration
from smarter.reports.student_administration import get_academic_years, set_default_year_back


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
        defined_roles = [(Allow, 'STATE_EDUCATION_ADMINISTRATOR_1', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        # Set up context security
        dummy_session = create_test_session(['STATE_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_user_context([RoleRelation("STATE_EDUCATION_ADMINISTRATOR_1", get_unittest_tenant_name(), "NC", "228", "242")])

        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        testing.tearDown()

    def test_get_academic_years(self):
        state_code = 'NC'
        test_cases = [
            # year_back, expect_value
            (-1, [2015]),
            (0, [2015]),
            (1, [2015]),
            (2, [2015, 2012]),
            (5, [2015, 2012]),
        ]
        for year_back, expect in test_cases:
            results = get_academic_years(state_code, year_back)
            self.assertEqual(expect, results, "%d most recent academic year should be %r" % (year_back, expect))

    def test_set_default_year_back(self):
        self.assertEqual(student_administration.DEFAULT_YEAR_BACK, 1, "Default number of year back should be 1")
        test_cases = [
            (None, 1),
            (-1, -1),
            (3, 3)
        ]
        for year_back, expect in test_cases:
            set_default_year_back(year_back)
            self.assertEqual(expect, student_administration.DEFAULT_YEAR_BACK, "default year back not equal")
