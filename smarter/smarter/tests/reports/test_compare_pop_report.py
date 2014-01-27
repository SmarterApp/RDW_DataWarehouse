'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.compare_pop_report import get_comparing_populations_report,\
    ComparingPopReport, CACHE_REGION_PUBLIC_DATA,\
    CACHE_REGION_PUBLIC_FILTERING_DATA, get_comparing_populations_cache_route,\
    set_default_min_cell_size
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.reports.helpers.constants import Constants, AssessmentType
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.session import Session
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.reports.helpers import filters


class TestComparingPopulations(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
        dummy_session = Session()
        dummy_session.set_session_id('123')
        dummy_session.set_roles(['TEACHER'])
        dummy_session.set_uid('272')
        dummy_session.set_tenant(get_unittest_tenant_name())
        self.__config.testing_securitypolicy(dummy_session)
        set_default_min_cell_size(0)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_school_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '228'
        testParam[Constants.SCHOOLGUID] = '242'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.METADATA in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check grade-level results
        records = results[Constants.RECORDS]
        self.assertEqual(1, len(records), "1 grade in the list")
        self.assertEqual('3', records[0][Constants.ID])
        self.assertEqual('3', records[0][Constants.NAME])
        asmt_results = records[0][Constants.RESULTS]
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results[Constants.SUBJECT1]
        self.assertEqual(35, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(11, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(4, intervals[0][Constants.COUNT])

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(35, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(11, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(4, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(3, len(context_items))
        self.assertEqual('New York', context_items[0][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[1][Constants.NAME])
        self.assertEqual('Sunset - Eastern Elementary', context_items[2][Constants.NAME])

        # check colors
        self.assertTrue('text_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])
        self.assertTrue('bg_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])

    def test_district_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '228'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.METADATA in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check school-level results
        records = results[Constants.RECORDS]
        self.assertEqual(3, len(records), "3 schools in the list")
        found_school = False
        for record in records:
            if record[Constants.ID] == '242':
                found_school = True
                self.assertEqual('Sunset - Eastern Elementary', record[Constants.NAME])
                asmt_results = record[Constants.RESULTS]
                self.assertEqual(2, len(asmt_results))
                subject1 = asmt_results[Constants.SUBJECT1]
                self.assertEqual(35, subject1[Constants.TOTAL])
                self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
                intervals = subject1[Constants.INTERVALS]
                self.assertEqual(4, len(intervals))
                self.assertEqual(1, intervals[0][Constants.LEVEL])
                self.assertEqual(11, intervals[0][Constants.PERCENTAGE])
                self.assertEqual(4, intervals[0][Constants.COUNT])
                break
        self.assertTrue(found_school, 'Did not find school in list')

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(56, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(14, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(8, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(2, len(context_items))
        self.assertEqual('New York', context_items[0][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[1][Constants.NAME])

        # check colors
        self.assertTrue('text_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])
        self.assertTrue('bg_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])

    def test_state_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.METADATA in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check district-level results
        records = results[Constants.RECORDS]
        self.assertEqual(5, len(records), "5 districts in the list")
        found_district = False
        for record in records:
            if record[Constants.ID] == '228':
                found_district = True
                self.assertEqual('Sunset School District', record[Constants.NAME])
                asmt_results = record[Constants.RESULTS]
                self.assertEqual(2, len(asmt_results))
                subject1 = asmt_results[Constants.SUBJECT1]
                self.assertEqual(56, subject1[Constants.TOTAL])
                self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
                intervals = subject1[Constants.INTERVALS]
                self.assertEqual(4, len(intervals))
                self.assertEqual(1, intervals[0][Constants.LEVEL])
                self.assertEqual(14, intervals[0][Constants.PERCENTAGE])
                self.assertEqual(8, intervals[0][Constants.COUNT])
                break
        self.assertTrue(found_district, 'Did not find district in list')

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(480, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(6, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(30, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(1, len(context_items))
        self.assertEqual('New York', context_items[0][Constants.NAME])

        # check colors
        self.assertEqual(len(results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS]), 4)
        self.assertTrue('text_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])
        self.assertTrue('bg_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])

    def test_invalid_params(self):
        params = {Constants.STATECODE: 'AA'}
        actual = get_comparing_populations_report(params)['records']
        self.assertListEqual([], actual, "Should return no results")

    def test_cache_route_without_filters(self):
        cpop = ComparingPopReport()
        name = get_comparing_populations_cache_route(cpop)
        self.assertEquals(name, CACHE_REGION_PUBLIC_DATA)

    def test_cache_route_with_filter(self):
        cpop = ComparingPopReport(**{'test': 'test'})
        name = get_comparing_populations_cache_route(cpop)
        self.assertEquals(name, CACHE_REGION_PUBLIC_FILTERING_DATA)

    def test_state_view_with_504_yes(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[filters.FILTERS_PROGRAM_504] = ['Y']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 1)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 20)
        self.assertEqual(results['records'][0]['results']['subject2']['total'], 20)

    def test_state_view_with_504_no(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[filters.FILTERS_PROGRAM_504] = ['N']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 5)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 134)
        self.assertEqual(results['records'][2]['results']['subject2']['total'], 139)

    def test_state_view_with_504_not_stated(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[filters.FILTERS_PROGRAM_504] = ['NS']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)

    def test_state_view_with_iep_yes(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[filters.FILTERS_PROGRAM_IEP] = ['Y']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 5)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 6)
        self.assertEqual(results['records'][4]['results']['subject2']['total'], 12)

    def test_state_view_with_iep_yes_504_no(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[filters.FILTERS_PROGRAM_IEP] = ['Y']
        testParam[filters.FILTERS_PROGRAM_504] = ['N']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 5)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 15)
        self.assertEqual(results['records'][2]['results']['subject2']['total'], 20)

    def test_filters_with_no_results(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[filters.FILTERS_PROGRAM_504] = ['NS']
        testParam[filters.FILTERS_PROGRAM_IEP] = ['NS']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)

    def test_district_view_with_grades(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_GRADE] = ['3']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)
        self.assertEqual(len(results['records']), 1)

    def test_view_with_multi_grades(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_GRADE] = ['3', '6', '7', '11']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)
        self.assertEqual(results['records'][2]['results']['subject1']['total'], 3)
        self.assertEqual(len(results['records']), 3)

    def test_view_with_lep_yes(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = 'c912df4b-acdf-40ac-9a91-f66aefac7851'
        testParam[filters.FILTERS_PROGRAM_LEP] = ['Y']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)

    def test_view_with_lep_no(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = 'c912df4b-acdf-40ac-9a91-f66aefac7851'
        testParam[filters.FILTERS_PROGRAM_LEP] = ['N']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 3)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 16)

    def test_view_with_lep_multi(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = 'c912df4b-acdf-40ac-9a91-f66aefac7851'
        testParam[filters.FILTERS_PROGRAM_LEP] = ['N', 'Y', 'NS']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 3)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 17)

    def test_comparing_populations_min_cell_size(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_ETHNICITY] = [filters.FILTERS_ETHNICITY_HISPANIC]
        # TODO: Fix this when metadata has the correct value set
        # We probably don't need to set the default min cell size after we set a value in csv
#        set_default_min_cell_size(5)
#        results = get_comparing_populations_report(testParam)
#        self.assertEqual(len(results['records']), 3)
#        # total must be filtered out
#        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)
#        self.assertEqual(results['records'][0]['results']['subject1']['intervals'][0]['percentage'], -1)
#        self.assertEqual(results['records'][0]['results']['subject1']['intervals'][1]['percentage'], -1)
#        self.assertEqual(results['records'][0]['results']['subject1']['intervals'][2]['percentage'], -1)
#        self.assertEqual(results['records'][0]['results']['subject1']['intervals'][3]['percentage'], -1)
#        set_default_min_cell_size(0)

    def test_comparing_populations_with_gender(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_GENDER] = [filters.FILTERS_GENDER_MALE]
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 3)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 8)
        self.assertEqual(results['records'][0]['results']['subject2']['total'], 8)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], -1)
        self.assertEqual(results['records'][1]['results']['subject2']['total'], -1)

    def test_comparing_populations_with_gender_not_stated(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_GENDER] = [filters.FILTERS_GENDER_NOT_STATED]
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 1)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)
        self.assertEqual(results['records'][0]['results']['subject2']['total'], -1)

    def test_comparing_populations_with_not_stated_count(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTTYPE] = AssessmentType.SUMMATIVE
        results = get_comparing_populations_report(testParam)
        self.assertEqual(results['not_stated']['total'], 47)
        self.assertEqual(results['not_stated']['dmgPrg504'], 3)
        self.assertEqual(results['not_stated']['dmgPrgIep'], 3)
        self.assertEqual(results['not_stated']['dmgPrgLep'], 1)
        self.assertEqual(results['not_stated']['ethnicity'], 1)
        self.assertEqual(results['not_stated']['gender'], 1)

    def test_filter_with_unfiltered_results(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_GENDER] = [filters.FILTERS_GENDER_MALE]
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 3)
        self.assertEqual(results['records'][0]['results']['subject1']['unfilteredTotal'], 18)
        self.assertEqual(results['records'][0]['results']['subject2']['unfilteredTotal'], 17)
        self.assertEqual(results['records'][1]['results']['subject1']['unfilteredTotal'], 3)
        self.assertEqual(results['records'][1]['results']['subject2']['unfilteredTotal'], 3)
        self.assertEqual(results['summary'][0]['results']['subject1']['unfilteredTotal'], 23)
        self.assertEqual(results['summary'][0]['results']['subject2']['unfilteredTotal'], 24)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
