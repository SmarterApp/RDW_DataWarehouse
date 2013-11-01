'''
Created on Jan 24, 2013

@author: tosako
'''
import unittest
from smarter.reports.extraction import _get_extract_assessment_query,\
    get_check_ela_interim_assessment_existence_query,\
    get_check_math_interim_assessment_existence_query,\
    get_check_ela_summative_assessment_existence_query,\
    get_check_math_summative_assessment_existence_query,\
    get_ela_interim_assessment_query,\
    get_math_interim_assessment_query,\
    get_ela_summative_assessment_query,\
    get_math_summative_assessment_query

from edapi.exceptions import NotFoundException
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.session import Session
from smarter.security.roles.teacher import Teacher  # @UnusedImport
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from edcore.tests.utils.unittest_with_edcore_sqlite import \
    Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name


class TestExtraction(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions':
            'public.data,public.filtered_data,public.shortlived'
        }

        CacheManager(**parse_cache_config_options(cache_opts))

        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
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

    def test_get_check_ela_interim_assessment_existence_query(self):
        query = get_check_ela_interim_assessment_existence_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 1)

    def test_get_check_math_interim_assessment_existence_query(self):
        query = get_check_math_interim_assessment_existence_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 1)

    def test_get_check_ela_summative_assessment_existence_query(self):
        query = get_check_ela_summative_assessment_existence_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 1)

    def test_get_check_math_summative_assessment_existence_query(self):
        query = get_check_math_summative_assessment_existence_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 1)

    def test_get_ela_interim_assessment_query(self):
        query = get_ela_interim_assessment_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 86)

    def test_get_math_interim_assessment_query(self):
        query = get_math_interim_assessment_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 94)

    def test_get_ela_summative_assessment_query(self):
        query = get_ela_summative_assessment_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 449)

    def test_get_math_summative_assessment_query(self):
        query = get_math_summative_assessment_query(2015)
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 480)

    def test_get_extract_assessment_query(self):
        query = _get_extract_assessment_query({})
        with UnittestEdcoreDBConnection() as connection:
            result = connection.execute(query).fetchall()
            self.assertEqual(len(result), 0)
