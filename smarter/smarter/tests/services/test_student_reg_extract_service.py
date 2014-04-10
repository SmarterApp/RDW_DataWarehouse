__author__ = 'ablum'

from pyramid.testing import DummyRequest
from pyramid import testing
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from pyramid.registry import Registry
from edextract.celery import setup_celery
from edapi.httpexceptions import EdApiHTTPPreconditionFailed

from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
import smarter.extracts.format
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edauth.security.user import RoleRelation
from edcore.security.tenant import set_tenant_map
from smarter.services.student_reg_extract_service import post_sr_stat_extract_service, post_sr_comp_extract_service
from mock import patch


class TestStudentRegExtract(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        reg.settings = {}
        reg.settings['extract.available_grades'] = '3,4,5,6,7,8,9,11'
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self.__tenant_name = get_unittest_tenant_name()

        defined_roles = [(Allow, 'STATE_EDUCATION_ADMINISTRATOR_1', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        # Set up context security
        dummy_session = create_test_session(['STATE_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_user_context([RoleRelation("STATE_EDUCATION_ADMINISTRATOR_1", get_unittest_tenant_name(), "NC", "228", "242")])

        self.__config.testing_securitypolicy(dummy_session)
        # celery settings for UT
        settings = {'extract.celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)
        # for UT purposes
        smarter.extracts.format.json_column_mapping = {}
        set_tenant_map({'tomcat': 'NC'})

    def tearDown(self):
        self.__request = None
        testing.tearDown()

    def test_post_sr_stat_extraction_request_invalid_params(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'academic_year': [2015]}

        self.assertRaises(EdApiHTTPPreconditionFailed, None, post_sr_stat_extract_service, self.__request)

    def test_post_sr_invalid_type(self):
        self.__request.method = 'POST'
        self.__request.json_body = {'extractType': ['studentRegistrationComp'], 'academicYear': [2015], "stateCode": ["NC"]}
        self.assertRaises(EdApiHTTPPreconditionFailed, None, post_sr_comp_extract_service, self.__request)

    @patch('smarter.services.student_reg_extract_service.process_async_extraction_request')
    def test_post_sr_comp_extraction_request(self, test_patch):
        test_patch.return_value = 'Mocked Method Called'

        self.__request.method = 'POST'
        self.__request.json_body = {'extractType': ['studentRegistrationCompletion'], 'academicYear': [2015], "stateCode": ["NC"]}
        response = post_sr_stat_extract_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.body, encoding='UTF-8'), '"Mocked Method Called"')

    @patch('smarter.services.student_reg_extract_service.process_async_extraction_request')
    def test_post_sr_stat_extraction_request(self, test_patch):
        test_patch.return_value = 'Mocked Method Called'

        self.__request.method = 'POST'
        self.__request.json_body = {'extractType': ['studentRegistrationStatistics'], 'academicYear': [2015], "stateCode": ["NC"]}
        response = post_sr_stat_extract_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.body, encoding='UTF-8'), '"Mocked Method Called"')
