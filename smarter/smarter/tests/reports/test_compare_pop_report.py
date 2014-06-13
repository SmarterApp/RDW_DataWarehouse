'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest

from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.security import Allow
from pyramid.httpexceptions import HTTPForbidden

from smarter.reports.compare_pop_report import get_comparing_populations_report,\
    ComparingPopReport, CACHE_REGION_PUBLIC_DATA,\
    CACHE_REGION_PUBLIC_FILTERING_DATA, get_comparing_populations_cache_route,\
    set_default_min_cell_size, get_merged_report_records
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from smarter.reports.helpers.constants import Constants, AssessmentType
from smarter.reports.helpers import filters
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport


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
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        self.__config.testing_securitypolicy(dummy_session.get_user())
        set_default_min_cell_size(0)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_school_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '228'
        testParam[Constants.ASMTYEAR] = 2016
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
        self.assertEqual(2, len(records), "2 grades in the list")
        self.assertEqual('3', records[0][Constants.ID])
        self.assertEqual('3', records[0][Constants.NAME])
        asmt_results = records[0][Constants.RESULTS]
        self.assertEqual(2, len(asmt_results))
        subject1 = asmt_results[Constants.SUBJECT1]
        self.assertEqual(21, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(10, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(2, intervals[0][Constants.COUNT])

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(35, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(14, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(5, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(4, len(context_items))
        self.assertEqual('Home', context_items[0][Constants.NAME])
        self.assertEqual('North Carolina', context_items[1][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[2][Constants.NAME])
        self.assertEqual('Sunset - Eastern Elementary', context_items[3][Constants.NAME])

        # check colors
        self.assertTrue('text_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])
        self.assertTrue('bg_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])

    def test_district_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '228'
        testParam[Constants.ASMTYEAR] = 2016
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
                self.assertEqual(14, intervals[0][Constants.PERCENTAGE])
                self.assertEqual(5, intervals[0][Constants.COUNT])
                break
        self.assertTrue(found_school, 'Did not find school in list')

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(51, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(18, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(9, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(3, len(context_items))
        self.assertEqual('North Carolina', context_items[1][Constants.NAME])
        self.assertEqual('Sunset School District', context_items[2][Constants.NAME])

        # check colors
        self.assertTrue('text_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])
        self.assertTrue('bg_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])

    def test_state_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2016
        results = get_comparing_populations_report(testParam)

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.METADATA in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check district-level results
        records = results[Constants.RECORDS]
        self.assertEqual(5, len(records), "4 districts in the list")
        found_district = False
        for record in records:
            if record[Constants.ID] == '228':
                found_district = True
                self.assertEqual('Sunset School District', record[Constants.NAME])
                asmt_results = record[Constants.RESULTS]
                self.assertEqual(2, len(asmt_results))
                subject1 = asmt_results[Constants.SUBJECT1]
                self.assertEqual(51, subject1[Constants.TOTAL])
                self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
                intervals = subject1[Constants.INTERVALS]
                self.assertEqual(4, len(intervals))
                self.assertEqual(1, intervals[0][Constants.LEVEL])
                self.assertEqual(18, intervals[0][Constants.PERCENTAGE])
                self.assertEqual(9, intervals[0][Constants.COUNT])
                break
        self.assertTrue(found_district, 'Did not find district in list')

        # check summary results
        summ_results = results[Constants.SUMMARY][0][Constants.RESULTS]
        self.assertEqual(2, len(summ_results))
        subject1 = summ_results[Constants.SUBJECT1]
        self.assertEqual(92, subject1[Constants.TOTAL])
        self.assertEqual(Constants.MATH, subject1[Constants.ASMT_SUBJECT])
        intervals = subject1[Constants.INTERVALS]
        self.assertEqual(4, len(intervals))
        self.assertEqual(1, intervals[0][Constants.LEVEL])
        self.assertEqual(13, intervals[0][Constants.PERCENTAGE])
        self.assertEqual(12, intervals[0][Constants.COUNT])

        # check subjects
        self.assertEqual(Constants.MATH, results[Constants.SUBJECTS][Constants.SUBJECT1])
        self.assertEqual(Constants.ELA, results[Constants.SUBJECTS][Constants.SUBJECT2])

        # check context
        context_items = results['context']['items']
        self.assertEqual(2, len(context_items))
        self.assertEqual('North Carolina', context_items[1][Constants.NAME])

        # check colors
        self.assertEqual(len(results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS]), 4)
        self.assertTrue('text_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])
        self.assertTrue('bg_color' in results[Constants.METADATA][Constants.SUBJECT1][Constants.COLORS][0])

    def test_invalid_params(self):
        params = {Constants.STATECODE: 'AA'}
        results = get_comparing_populations_report(params)
        self.assertIsInstance(results, HTTPForbidden)

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
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_PROGRAM_504] = ['Y']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 1)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 20)
        self.assertEqual(results['records'][0]['results']['subject2']['total'], 20)

    def test_state_view_with_504_no(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2015
        testParam[filters.FILTERS_PROGRAM_504] = ['N']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 4)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 97)
        self.assertEqual(results['records'][1]['results']['subject2']['total'], 66)

    def test_state_view_with_504_not_stated(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_PROGRAM_504] = ['NS']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)

    def test_state_view_with_iep_yes(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_PROGRAM_IEP] = ['Y']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 3)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 4)
        self.assertEqual(results['records'][1]['results']['subject2']['total'], -1)

    def test_state_view_with_iep_yes_504_no(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2015
        testParam[filters.FILTERS_PROGRAM_IEP] = ['Y']
        testParam[filters.FILTERS_PROGRAM_504] = ['N']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 4)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 11)
        self.assertEqual(results['records'][1]['results']['subject2']['total'], -1)

    def test_filters_with_no_results(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_PROGRAM_504] = ['NS']
        testParam[filters.FILTERS_PROGRAM_IEP] = ['NS']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)

    def test_district_view_with_grades(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_GRADE] = ['3']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 0)
        self.assertEqual(len(results['records']), 1)

    def test_view_with_multi_grades(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_GRADE] = ['3', '6', '7', '11']
        results = get_comparing_populations_report(testParam)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 0)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 8)
        self.assertEqual(len(results['records']), 3)

    def test_view_with_lep_yes(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '0513ba44-e8ec-4186-9a0e-8481e9c16206'
        testParam[filters.FILTERS_PROGRAM_LEP] = ['Y']
        testParam[Constants.ASMTYEAR] = 2015
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 4)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], 3)

    def test_view_with_lep_no(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '0513ba44-e8ec-4186-9a0e-8481e9c16206'
        testParam[filters.FILTERS_PROGRAM_LEP] = ['N']
        testParam[Constants.ASMTYEAR] = 2015
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 4)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 53)

    def test_view_with_lep_multi(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '0513ba44-e8ec-4186-9a0e-8481e9c16206'
        testParam[filters.FILTERS_PROGRAM_LEP] = ['N', 'Y', 'NS']
        testParam[Constants.ASMTYEAR] = 2015
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 4)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], 55)

    def test_comparing_populations_min_cell_size(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
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

    def test_comparing_populations_with_sex(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_SEX] = [filters.FILTERS_SEX_MALE]
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)
        self.assertEqual(results['records'][0]['results']['subject2']['total'], 5)
        self.assertEqual(results['records'][1]['results']['subject1']['total'], -1)
        self.assertEqual(results['records'][1]['results']['subject2']['total'], 0)

    def test_comparing_populations_with_sex_not_stated(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[filters.FILTERS_SEX] = [filters.FILTERS_SEX_NOT_STATED]
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 1)
        self.assertEqual(results['records'][0]['results']['subject1']['total'], -1)
        self.assertEqual(results['records'][0]['results']['subject2']['total'], 0)

    def test_comparing_populations_with_not_stated_count(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTTYPE] = AssessmentType.SUMMATIVE
        results = get_comparing_populations_report(testParam)

        self.assertEqual(results['not_stated']['total'], 29)
        self.assertEqual(results['not_stated']['dmgPrg504'], 2)
        self.assertEqual(results['not_stated']['dmgPrgIep'], 2)
        self.assertEqual(results['not_stated']['dmgPrgLep'], 0)
        self.assertEqual(results['not_stated']['ethnicity'], 0)
        self.assertEqual(results['not_stated']['sex'], 1)

    def test_filter_with_unfiltered_results(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTYEAR] = 2016
        testParam[filters.FILTERS_SEX] = [filters.FILTERS_SEX_MALE]
        results = get_comparing_populations_report(testParam)
        self.assertEqual(len(results['records']), 2)
        self.assertEqual(results['records'][0]['results']['subject1']['unfilteredTotal'], 10)
        self.assertEqual(results['records'][0]['results']['subject2']['unfilteredTotal'], 9)
        self.assertEqual(results['records'][1]['results']['subject1']['unfilteredTotal'], 3)
        self.assertEqual(results['records'][1]['results']['subject2']['unfilteredTotal'], -1)
        self.assertEqual(results['summary'][0]['results']['subject1']['unfilteredTotal'], 15)
        self.assertEqual(results['summary'][0]['results']['subject2']['unfilteredTotal'], 14)

    def test_get_merged_report_records(self):
        summative = {'records': [{'id': 'a', 'name': 'a', 'type': 'sum',
                                  'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}},
                                 {'id': 'b', 'name': 'b', 'type': 'sum',
                                  'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}}],
                     'subjects': {'a': 'a'}}
        interim = {'records': [{'id': 'a', 'name': 'a', 'type': 'int',
                                'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}},
                               {'id': 'b', 'name': 'b', 'type': 'int',
                                'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}}],
                   'subjects': {'a': 'a'}}
        results = get_merged_report_records(summative, interim)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['type'], 'sum')
        self.assertEqual(results[0]['name'], 'a')
        self.assertEqual(results[1]['type'], 'sum')
        self.assertEqual(results[1]['name'], 'b')

    def test_get_merged_report_records_with_no_summative(self):
        summative = {'records': [],
                     'subjects': {'a': 'a'}}
        interim = {'records': [{'id': 'a', 'name': 'a', 'type': 'int',
                                'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}},
                               {'id': 'b', 'name': 'b', 'type': 'int',
                                'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}}],
                   'subjects': {'a': 'a'}}
        results = get_merged_report_records(summative, interim)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['type'], 'int')
        self.assertEqual(results[0]['name'], 'a')
        self.assertEqual(results[1]['type'], 'int')
        self.assertEqual(results[1]['name'], 'b')

    def test_get_merged_report_records_with_mixed_asmt_types(self):
        summative = {'records': [{'id': 'b', 'name': 'b', 'type': 'sum',
                                  'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}}],
                     'subjects': {'a': 'a'}}
        interim = {'records': [{'id': 'a', 'name': 'a', 'type': 'int',
                                'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}},
                               {'id': 'b', 'name': 'b', 'type': 'int',
                                'results': {'a': {'total': 3, 'intervals': [{'percentage': 100}]}}}],
                   'subjects': {'a': 'a'}}
        results = get_merged_report_records(summative, interim)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['type'], 'int')
        self.assertEqual(results[0]['name'], 'a')
        self.assertEqual(results[1]['type'], 'sum')
        self.assertEqual(results[1]['name'], 'b')

    def test_get_merged_report_records_with_interim(self):
        summative = {'records': [{'id': 'b', 'name': 'b', 'type': 'sum',
                                  'results': {'a': {'total': 0, 'intervals': [{'percentage': 0}]}}}],
                     'subjects': {'a': 'a'}}
        interim = {'records': [{'id': 'b', 'name': 'b', 'type': 'int',
                                'results': {'a': {'total': -1, 'hasInterim': True, 'intervals': [{'percentage': -1}]}}}],
                   'subjects': {'a': 'a'}}
        results = get_merged_report_records(summative, interim)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['type'], 'sum')
        self.assertEqual(results[0]['name'], 'b')
        self.assertEqual(results[0]['results']['a']['hasInterim'], True)

    def test_get_merged_report_records_with_no_results(self):
        summative = {'records': [{'id': 'b', 'name': 'b', 'type': 'sum',
                                  'results': {'a': {'total': 0, 'intervals': [{'percentage': 0}]}}}],
                     'subjects': {'a': 'a'}}
        interim = {'records': [{'id': 'b', 'name': 'b', 'type': 'int',
                                'results': {'a': {'total': 3, 'hasInterim': True, 'intervals': [{'percentage': 100}]}}}],
                   'subjects': {'a': 'a'}}
        results = get_merged_report_records(summative, interim)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['type'], 'sum')
        self.assertEqual(results[0]['name'], 'b')
        self.assertEqual(results[0]['results']['a']['hasInterim'], True)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
