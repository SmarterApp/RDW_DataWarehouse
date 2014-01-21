'''
Created on Nov 5, 2013

@author: ejen
'''
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.session import Session
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from edcore.tests.utils.unittest_with_edcore_sqlite import \
    Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.extracts.processor import process_async_extraction_request, \
    get_extract_file_path, get_extract_work_zone_path, \
    get_encryption_public_key_identifier, get_archive_file_path, get_gatekeeper, \
    get_pickup_zone_info, process_sync_extract_request, \
    get_asmt_metadata_file_path, _prepare_data, _create_tasks, \
    _create_asmt_metadata_task, _create_new_task, \
    _get_extract_work_zone_base_dir, _get_extract_request_user_info, \
    _create_tasks_with_responses
from pyramid.registry import Registry
from edapi.exceptions import NotFoundException
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
import tempfile
from edextract.celery import setup_celery
import smarter
from sqlalchemy.sql.expression import select
from edauth.security.user import User
from smarter.extracts.constants import Constants as Extract
from edextract.tasks.constants import Constants as TaskConstants
from beaker.cache import CacheManager, cache_managers
from beaker.util import parse_cache_config_options


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
        settings = {'extract.celery.CELERY_ALWAYS_EAGER': True}
        setup_celery(settings)
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        # Set up context security
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(),
                               user_id='272', guid='272')
        dummy_session = Session()
        dummy_session.set_roles(['STATE_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_uid('272')
        dummy_session.set_tenant(get_unittest_tenant_name())
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())
        cache_managers.clear()

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def test_process_extraction_async_request(self):
        params = {'stateCode': ['CA'],
                  'asmtYear': ['2015'],
                  'asmtType': ['SUMMATIVE', 'INTERIM COMPREHENSIVE'],
                  'asmtSubject': ['Math', 'ELA'],
                  'extractType': ['studentAssessment']}
        results = process_async_extraction_request(params)
        tasks = results['tasks']
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0]['status'], 'fail')
        self.assertEqual(tasks[3]['status'], 'fail')

    def test_get_file_name_tenant_level(self):
        params = {'stateCode': 'CA',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259',
                  'asmtGrade': '6'}
        path = get_extract_file_path(params, 'tenant', 'request_id', is_tenant_level=True)
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_CA_GRADE_6_UUUU_ABC_', path)
        self.assertIn('2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.csv', path)

    def test_get_file_name_school(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259',
                  'asmtType': 'abc',
                  'asmtGrade': '1'}
        path = get_extract_file_path(params, 'tenant', 'request_id')
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_GRADE_1_UUUU_ABC_', path)
        self.assertIn('2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.csv', path)

    def test_get_file_name_grade(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        path = get_extract_file_path(params, 'tenant', 'request_id')
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_GRADE_5_UUUU_ABC_', path)
        self.assertIn('2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.csv', path)

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

    def test_process_sync_extraction_request_NotFoundException(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': [],
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        self.assertRaises(NotFoundException, process_sync_extract_request, params)

    def test_process_sync_extraction_request_NotFoundException_with_subject(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': ['ELA'],
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        self.assertRaises(NotFoundException, process_sync_extract_request, params)

    def test_process_sync_extraction_request_with_subject(self):
        params = {'stateCode': 'NY',
                  'districtGuid': 'c912df4b-acdf-40ac-9a91-f66aefac7851',
                  'schoolGuid': 'fc85bac1-f471-4425-8848-c6cb28058614',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': ['ELA'],
                  'asmtGuid': 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0'}
        zip_data = process_sync_extract_request(params)
        self.assertIsNotNone(zip_data)

    def test_process_async_extraction_request_with_subject(self):
        params = {'stateCode': ['NY'],
                  'asmtYear': ['2015'],
                  'districtGuid': 'c912df4b-acdf-40ac-9a91-f66aefac7851',
                  'schoolGuid': 'fc85bac1-f471-4425-8848-c6cb28058614',
                  'asmtType': ['SUMMATIVE'],
                  'asmtSubject': ['ELA'],
                  'asmtGrade': ['3'],
                  'asmtGuid': 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0'}
        response = process_async_extraction_request(params)
        self.assertIn('.zip.gpg', response['fileName'])
        self.assertEqual(response['tasks'][0]['status'], 'ok')

    def test___prepare_data(self):
        params = {'stateCode': 'NY',
                  'districtGuid': 'c912df4b-acdf-40ac-9a91-f66aefac7851',
                  'schoolGuid': 'fc85bac1-f471-4425-8848-c6cb28058614',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'ELA',
                  'asmtGuid': 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0'}
        smarter.extracts.format.json_column_mapping = {}
        guid_grade, dim_asmt, fact_asmt_outcome = _prepare_data(params)
        self.assertEqual(1, len(guid_grade))
        self.assertIsNotNone(dim_asmt)
        self.assertIsNotNone(fact_asmt_outcome)
        (guid, grade) = guid_grade[0]
        self.assertEqual(guid, 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0')
        self.assertEqual(grade, '11')

    def test_get_asmt_metadata_file_path(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        file_name = get_asmt_metadata_file_path(params, "tenant", "id")
        self.assertIn('/tmp/work_zone/tenant/id/data', file_name)
        self.assertIn('METADATA_ASMT_CA_GRADE_5_UUUU_ABC_2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.json', file_name)

    def test__create_tasks_for_non_tenant_lvl(self):
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            fact = connection.get_table('fact_asmt_outcome')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        results = _create_tasks('request_id', user, 'tenant', params, query)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        self.assertFalse(results[0][TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertTrue(results[1][TaskConstants.TASK_IS_JSON_REQUEST])

    def test__create_tasks_for_tenant_lvl(self):
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            fact = connection.get_table('fact_asmt_outcome')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        results = _create_tasks('request_id', user, 'tenant', params, query, is_tenant_level=True)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        self.assertFalse(results[0][TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertTrue(results[1][TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_CA_GRADE_5', results[0][TaskConstants.TASK_FILE_NAME])

    def test__create_asmt_metadata_task(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        task = _create_asmt_metadata_task('request_id', user, 'tenant', params)
        self.assertIsNotNone(task)
        self.assertTrue(task[TaskConstants.TASK_IS_JSON_REQUEST])

    def test__create_new_task_non_tenant_level(self):
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            fact = connection.get_table('fact_asmt_outcome')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=False, is_tenant_level=False)
        self.assertIsNotNone(task)
        self.assertFalse(task[TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_GRADE_5', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_non_tenant_level_json_request(self):
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            fact = connection.get_table('fact_asmt_outcome')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=True, is_tenant_level=False)
        self.assertIsNotNone(task)
        self.assertTrue(task[TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/METADATA_ASMT_CA_GRADE_5_UUUU_ABC_2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.json', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_tenant_level(self):
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            fact = connection.get_table('fact_asmt_outcome')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=False, is_tenant_level=True)
        self.assertIsNotNone(task)
        self.assertFalse(task[TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_CA_GRADE_5', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_tenant_level_json_request(self):
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            fact = connection.get_table('fact_asmt_outcome')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        user.set_tenant('tenant')
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=True, is_tenant_level=True)
        self.assertIsNotNone(task)
        self.assertTrue(task[TaskConstants.TASK_IS_JSON_REQUEST])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/METADATA_ASMT_CA_GRADE_5_UUUU_ABC_2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.json', task[TaskConstants.TASK_FILE_NAME])

    def test__get_extract_work_zone_base_dir(self):
        self.assertEqual('/tmp/work_zone', _get_extract_work_zone_base_dir())

    def test___get_extract_request_user_info(self):
        result = _get_extract_request_user_info()
        self.assertIsInstance(result[0], str)
        self.assertEqual('testtenant', result[2])

    def test__create_tasks_with_responses_non_tenant_level(self):
        params = {'stateCode': 'NY',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtGrade': '3',
                  'asmtSubject': 'Math',
                  'asmtType': 'SUMMATIVE'}
        user = User()
        user.set_tenant('tenant')
        results = _create_tasks_with_responses('request_id', user, 'tenant', params, is_tenant_level=False)
        self.assertEqual(len(results[0]), 2)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0][Extract.STATUS], Extract.OK)

    def test__create_tasks_with_responses_non_tenant_level_no_data(self):
        params = {'stateCode': 'NY',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtGrade': '3',
                  'asmtSubject': 'NoSubject',
                  'asmtType': 'SUMMATIVE'}
        user = User()
        user.set_tenant('tenant')
        results = _create_tasks_with_responses('request_id', user, 'tenant', params, is_tenant_level=False)
        self.assertEqual(len(results[0]), 0)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0][Extract.STATUS], Extract.FAIL)

    def test__create_tasks_with_responses_tenant_level(self):
        params = {'stateCode': 'NY',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtSubject': 'Math',
                  'asmtType': 'SUMMATIVE'}
        user = User()
        user.set_tenant('tenant')
        results = _create_tasks_with_responses('request_id', user, 'tenant', params, is_tenant_level=False)
        self.assertEqual(len(results[0]), 2)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0][Extract.STATUS], Extract.OK)
