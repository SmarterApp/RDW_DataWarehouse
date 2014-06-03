from pyramid.testing import DummyRequest
from pyramid import testing
from edcore.tests.utils.unittest_with_edcore_sqlite import \
    Unittest_with_edcore_sqlite, \
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.extracts.student_asmt_processor import process_async_extraction_request, \
    process_async_item_extraction_request, get_items_extract_file_path, \
    get_extract_file_path, process_sync_extract_request, process_sync_item_extract_request, \
    get_asmt_metadata_file_path, _prepare_data, _create_tasks, \
    _create_asmt_metadata_task, _create_new_task, \
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
from edextract.tasks.constants import Constants as TaskConstants, ExtractionDataType
from beaker.cache import CacheManager, cache_managers
from beaker.util import parse_cache_config_options
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edcore.security.tenant import set_tenant_map
from smarter.security.constants import RolesConstants
from unittest.mock import patch
from smarter.security.roles.pii import PII  # @UnusedImport


__author__ = 'ablum'


class TestStudentAsmtProcessor(Unittest_with_edcore_sqlite, Unittest_with_stats_sqlite):

    def setUp(self):
        self.reg = Registry()
        self.__work_zone_dir = tempfile.TemporaryDirectory()
        self.reg.settings = {'extract.work_zone_base_dir': '/tmp/work_zone',
                             'hpz.file_upload_base_url': 'http://somehost:82/files',
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
        defined_roles = [(Allow, RolesConstants.SAR_EXTRACTS, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        dummy_session = create_test_session([RolesConstants.SAR_EXTRACTS])
        self.__config.testing_securitypolicy(dummy_session.get_user())
        set_tenant_map({get_unittest_tenant_name(): 'NC'})

    def tearDown(self):
        # reset the registry
        testing.tearDown()
        cache_managers.clear()

    @classmethod
    def setUpClass(cls):
        Unittest_with_edcore_sqlite.setUpClass()
        Unittest_with_stats_sqlite.setUpClass()

    def test_process_extraction_async_request(self):
        params = {'stateCode': ['NC'],
                  'asmtYear': ['2018'],
                  'asmtType': ['SUMMATIVE', 'INTERIM COMPREHENSIVE'],
                  'asmtSubject': ['Math', 'ELA'],
                  'extractType': ['studentAssessment']}
        results = process_async_extraction_request(params)
        tasks = results['tasks']
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0]['status'], 'fail')
        self.assertEqual(tasks[3]['status'], 'fail')

    def test_process_async_item_extraction_request(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2018',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3',
                  'extractType': 'itemLevel'}
        results = process_async_item_extraction_request(params)
        tasks = results['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['status'], 'fail')

    def test_get_file_name_tenant_level(self):
        params = {'stateCode': 'CA',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259',
                  'asmtYear': '2015',
                  'asmtGrade': '6'}
        path = get_extract_file_path(params, 'tenant', 'request_id', is_tenant_level=True)
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_2015_CA_GRADE_6_UUUU_ABC_', path)
        self.assertIn('2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.csv', path)

    def test_get_file_name_school(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGrade': '1'}
        path = get_extract_file_path(params, 'tenant', 'request_id')
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_2015_GRADE_1_UUUU_ABC_', path)
        self.assertIn('2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.csv', path)

    def test_get_file_name_grade(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        path = get_extract_file_path(params, 'tenant', 'request_id')
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_2015_GRADE_5_UUUU_ABC_', path)
        self.assertIn('2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.csv', path)

    def test_get_item_file_name(self):
        params = {'stateCode': 'CA',
                  'asmtYear': '2015',
                  'asmtType': 'abc',
                  'asmtSubject': 'UUUU',
                  'asmtGrade': '5'}
        path = get_items_extract_file_path(params, 'tenant', 'request_id')
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ITEMS_CA_2015_ABC_UUUU_GRADE_5', path)

    def test_process_sync_extraction_request_NotFoundException(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': [],
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        self.assertRaises(NotFoundException, process_sync_extract_request, params)

    def test_process_sync_extraction_request_NotFoundException_with_subject(self):
        params = {'stateCode': 'NC',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': ['ELA'],
                  'asmtYear': '2018',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        self.assertRaises(NotFoundException, process_sync_extract_request, params)

    def test_process_sync_extraction_request_with_subject(self):
        params = {'stateCode': 'NC',
                  'districtGuid': 'c912df4b-acdf-40ac-9a91-f66aefac7851',
                  'schoolGuid': 'fc85bac1-f471-4425-8848-c6cb28058614',
                  'asmtType': 'INTERIM COMPREHENSIVE',
                  'asmtSubject': ['ELA'],
                  'asmtYear': '2016',
                  'asmtGuid': 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0'}
        zip_data = process_sync_extract_request(params)
        self.assertIsNotNone(zip_data)

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_process_async_extraction_request_with_subject(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        params = {'stateCode': ['NC'],
                  'asmtYear': ['2015'],
                  'districtGuid': 'c912df4b-acdf-40ac-9a91-f66aefac7851',
                  'schoolGuid': 'fc85bac1-f471-4425-8848-c6cb28058614',
                  'asmtType': ['SUMMATIVE'],
                  'asmtSubject': ['ELA'],
                  'asmtGrade': ['3'],
                  'asmtYear': ['2016'],
                  'asmtGuid': 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0'}
        response = process_async_extraction_request(params)
        self.assertIn('.zip', response['fileName'])
        self.assertNotIn('.gpg', response['fileName'])
        self.assertEqual(response['tasks'][0]['status'], 'ok')
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response['download_url'])

    def test_process_sync_items_extraction_request_NotFoundException(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2018',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'Math',
                  'asmtGrade': '3'}
        self.assertRaises(NotFoundException, process_sync_item_extract_request, params)

    def test_process_sync_items_extraction_request_with_subject(self):
        params = {'stateCode': 'NC',
                  'asmtYear': '2016',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'ELA',
                  'asmtGrade': '3'}
        zip_data = process_sync_item_extract_request(params)
        self.assertIsNotNone(zip_data)

    @patch('smarter.extracts.student_asmt_processor.register_file')
    def test_process_async_items_extraction_request_with_subject(self, register_file_patch):
        register_file_patch.return_value = 'a1-b2-c3-d4-e1e10', 'http://somehost:82/download/a1-b2-c3-d4-e1e10'
        params = {'stateCode': 'NC',
                  'asmtYear': '2016',
                  'asmtType': 'SUMMATIVE',
                  'asmtSubject': 'ELA',
                  'asmtGrade': '3'}
        response = process_async_item_extraction_request(params)
        self.assertIn('.zip', response['fileName'])
        self.assertNotIn('.gpg', response['fileName'])
        self.assertEqual(response['tasks'][0]['status'], 'ok')
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', response['download_url'])

    def test___prepare_data(self):
        params = {'stateCode': 'NC',
                  'districtGuid': 'c912df4b-acdf-40ac-9a91-f66aefac7851',
                  'schoolGuid': 'fc85bac1-f471-4425-8848-c6cb28058614',
                  'asmtType': 'INTERIM COMPREHENSIVE',
                  'asmtSubject': 'ELA',
                  'asmtGuid': 'c8f2b827-e61b-4d9e-827f-daa59bdd9cb0'}
        smarter.extracts.format.json_column_mapping = {}
        guid_grade, dim_asmt, fact_asmt_outcome_vw = _prepare_data(params)
        self.assertEqual(1, len(guid_grade))
        self.assertIsNotNone(dim_asmt)
        self.assertIsNotNone(fact_asmt_outcome_vw)
        (guid, grade) = guid_grade[0]
        self.assertEqual(guid, 'a685f0ec-a0a6-4b1e-93b8-0c4298ff6374')
        self.assertEqual(grade, '11')

    def test_get_asmt_metadata_file_path(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        file_name = get_asmt_metadata_file_path(params, "tenant", "id")
        self.assertIn('/tmp/work_zone/tenant/id/data', file_name)
        self.assertIn('METADATA_ASMT_2015_CA_GRADE_5_UUUU_ABC_2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.json', file_name)

    def test__create_tasks_for_non_tenant_lvl(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        results = _create_tasks('request_id', user, 'tenant', params, query)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        self.assertEquals(ExtractionDataType.QUERY_CSV, results[0][TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertEquals(ExtractionDataType.QUERY_JSON, results[1][TaskConstants.EXTRACTION_DATA_TYPE])

    def test__create_tasks_for_tenant_lvl(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        results = _create_tasks('request_id', user, 'tenant', params, query, is_tenant_level=True)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 2)
        self.assertEquals(ExtractionDataType.QUERY_CSV, results[0][TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertEquals(ExtractionDataType.QUERY_JSON, results[1][TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_2015_CA_GRADE_5', results[0][TaskConstants.TASK_FILE_NAME])

    def test__create_asmt_metadata_task(self):
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        task = _create_asmt_metadata_task('request_id', user, 'tenant', params)
        self.assertIsNotNone(task)
        self.assertEquals(ExtractionDataType.QUERY_JSON, task[TaskConstants.EXTRACTION_DATA_TYPE])

    def test__create_new_task_non_tenant_level(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=False, is_tenant_level=False,
                                extract_file_path=get_extract_file_path)
        self.assertIsNotNone(task)
        self.assertEquals(ExtractionDataType.QUERY_CSV, task[TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_2015_GRADE_5', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_non_tenant_level_json_request(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=True, is_tenant_level=False)
        self.assertIsNotNone(task)
        self.assertEquals(ExtractionDataType.QUERY_JSON, task[TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/METADATA_ASMT_2015_CA_GRADE_5_UUUU_ABC_2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.json', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_tenant_level(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=False, is_tenant_level=True,
                                extract_file_path=get_extract_file_path)
        self.assertIsNotNone(task)
        self.assertEquals(ExtractionDataType.QUERY_CSV, task[TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/ASMT_2015_CA_GRADE_5', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_tenant_level_json_request(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'districtGuid': '341',
                  'schoolGuid': 'asf',
                  'asmtGrade': '5',
                  'asmtSubject': 'UUUU',
                  'asmtType': 'abc',
                  'asmtYear': '2015',
                  'asmtGuid': '2C2ED8DC-A51E-45D1-BB4D-D0CF03898259'}
        user = User()
        task = _create_new_task('request_id', user, 'tenant', params, query, asmt_metadata=True, is_tenant_level=True)
        self.assertIsNotNone(task)
        self.assertEquals(ExtractionDataType.QUERY_JSON, task[TaskConstants.EXTRACTION_DATA_TYPE])
        self.assertIn('/tmp/work_zone/tenant/request_id/data/METADATA_ASMT_2015_CA_GRADE_5_UUUU_ABC_2C2ED8DC-A51E-45D1-BB4D-D0CF03898259.json', task[TaskConstants.TASK_FILE_NAME])

    def test__create_new_task_item_level(self):
        with UnittestEdcoreDBConnection() as connection:
            fact = connection.get_table('fact_asmt_outcome_vw')
            query = select([fact.c.student_guid], from_obj=[fact])
        params = {'stateCode': 'CA',
                  'asmtYear': '2015',
                  'asmtType': 'abc',
                  'asmtSubject': 'UUUU',
                  'asmtGrade': '5'}
        user = User()
        task = _create_new_task('request_id', user, 'tenant', params, query, item_level=True, is_tenant_level=True)
        self.assertIsNotNone(task)
        self.assertEquals(ExtractionDataType.QUERY_ITEMS_CSV, task[TaskConstants.EXTRACTION_DATA_TYPE])

    def test__create_tasks_with_responses_non_tenant_level(self):
        params = {'stateCode': 'NC',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtGrade': '3',
                  'asmtSubject': 'Math',
                  'asmtYear': '2016',
                  'asmtType': 'SUMMATIVE'}
        user = User()
        results = _create_tasks_with_responses('request_id', user, 'tenant', params, is_tenant_level=False)
        self.assertEqual(len(results[0]), 2)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0][Extract.STATUS], Extract.OK)

    def test__create_tasks_with_responses_non_tenant_level_no_data(self):
        params = {'stateCode': 'NC',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtGrade': '3',
                  'asmtSubject': 'NoSubject',
                  'asmtYear': '2015',
                  'asmtType': 'SUMMATIVE'}
        user = User()
        results = _create_tasks_with_responses('request_id', user, 'tenant', params, is_tenant_level=False)
        self.assertEqual(len(results[0]), 0)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0][Extract.STATUS], Extract.FAIL)

    def test__create_tasks_with_responses_tenant_level(self):
        params = {'stateCode': 'NC',
                  'districtGuid': '228',
                  'schoolGuid': '242',
                  'asmtSubject': 'Math',
                  'asmtYear': '2016',
                  'asmtType': 'SUMMATIVE'}
        user = User()
        results = _create_tasks_with_responses('request_id', user, 'tenant', params, is_tenant_level=False)
        self.assertEqual(len(results[0]), 4)
        self.assertEqual(len(results[1]), 1)
        self.assertEqual(results[1][0][Extract.STATUS], Extract.OK)
