'''
Created on Nov 5, 2013

@author: ejen
'''
from pyramid.testing import DummyRequest
from pyramid import testing
from edcore.tests.utils.unittest_with_edcore_sqlite import \
    Unittest_with_edcore_sqlite
from smarter.extracts.processor import get_extract_work_zone_path, \
    get_encryption_public_key_identifier, get_archive_file_path, get_gatekeeper, \
    get_pickup_zone_info, get_extract_request_user_info, _get_extract_work_zone_base_dir
from pyramid.registry import Registry
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
import tempfile

from beaker.cache import CacheManager, cache_managers
from beaker.util import parse_cache_config_options
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edcore.security.tenant import set_tenant_map


class TestProcessor(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.reg = Registry()
        self.__work_zone_dir = tempfile.TemporaryDirectory()
        self.reg.settings = {'extract.work_zone_base_dir': '/tmp/work_zone',
                             'pickup.gatekeeper.t1': '/t/acb',
                             'pickup.gatekeeper.t2': '/a/df',
                             'pickup.gatekeeper.y': '/a/c',
                             'pickup.sftp.hostname': 'hostname.local.net',
                             'pickup.sftp.user': 'myUser',
                             'pickup.sftp.private_key_file': '/home/users/myUser/.ssh/id_rsa',
                             'extract.available_grades': '3,4,5,6,7,8,11'}
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        dummy_session = create_test_session(['STATE_EDUCATION_ADMINISTRATOR_1'])
        defined_roles = [(Allow, 'STATE_EDUCATION_ADMINISTRATOR_1', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        self.__config.testing_securitypolicy(dummy_session.get_user())
        set_tenant_map({'tomcat': 'NC'})

    def tearDown(self):
        # reset the registry
        testing.tearDown()
        cache_managers.clear()

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def test_get_extract_work_zone_path(self):
        path = get_extract_work_zone_path('tenant', 'request')
        self.assertEqual(path, '/tmp/work_zone/tenant/request/data')

    def test_get_encryption_public_key_identifier(self):
        self.assertIsNone(get_encryption_public_key_identifier("tenant"))

    def test_get_archive_file_path(self):
        self.assertIn("/tmp/work_zone/tenant/requestId/zip/user", get_archive_file_path("user", "tenant", "requestId"))

    def test_get_archive_file_path_extension(self):
        filename = get_archive_file_path("user", "tenant", "requestId")
        self.assertIn('.zip.gpg', filename)

    def test_gatekeeper(self):
        config = self.reg.settings
        pickup = config.get('pickup.gatekeeper.t1')
        self.assertEqual(pickup, get_gatekeeper('t1'))
        self.assertEqual(None, get_gatekeeper('dne'))

    def test_get_pickup_zone_info(self):
        config = self.reg.settings
        host = config.get('pickup.sftp.hostname')
        user = config.get('pickup.sftp.user')
        private_key = config.get('pickup.sftp.private_key_file')
        pickup = get_pickup_zone_info('t1')
        self.assertEqual(host, pickup[0])
        self.assertEqual(user, pickup[1])
        self.assertEqual(private_key, pickup[2])

    def test_get_extract_request_user_info(self):
        result = get_extract_request_user_info('NC')
        self.assertIsInstance(result[0], str)
        self.assertEqual('tomcat', result[2])

    def test__get_extract_work_zone_base_dir(self):
        self.assertEqual('/tmp/work_zone', _get_extract_work_zone_base_dir())
