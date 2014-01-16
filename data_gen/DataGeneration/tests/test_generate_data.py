'''
Created on Aug 6, 2013

@author: swimberly
'''
from datetime import date
import unittest
import csv
import os
import shutil
from collections import Counter
from tempfile import mkdtemp

from DataGeneration.src.models.entities import (InstitutionHierarchy, Staff, Section, Assessment,
                                                AssessmentOutcome, ExternalUserStudent, Student)
import DataGeneration.src.generate_data as gd2
import DataGeneration.src.models.helper_entities as he
from DataGeneration.src.generators.generate_entities import generate_assessments
import DataGeneration.src.demographics.demographics as dmg
import DataGeneration.src.models.state_population as sp
from DataGeneration.src.generators.generate_helper_entities import generate_school
from DataGeneration.src.writers.output_asmt_outcome import initialize_csv_file

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Test(unittest.TestCase):

    def setUp(self):
        self.output_dir = mkdtemp()
        self.from_date = '20120901'
        self.to_date = None
        self.most_recent = True
        self.date_taken_year = '2012'

        self.entity_to_path_dict = {DummyEntity1: os.path.join(self.output_dir, 'dummy_ent_1.fortest'),
                                    DummyEntity2: os.path.join(self.output_dir, 'dummy_ent_2.fortest')}
        self.csv_file_names = {DummyEntity1: 'dummy_ent_1.fortest',
                               DummyEntity2: 'dummy_ent_2.fortest'}
        self.csv_file = write_demographics_csv(self.output_dir)
        self.demo_obj = dmg.Demographics(self.csv_file)
        self.demo_id = 'typical1'
        self.state_population = sp.StatePopulation('Test', 'TS', 'typical_1')
        self.state_population.populate_state(get_state_types()['typical_1'], get_district_types(), get_school_types())
        self.state_population.get_state_demographics(self.demo_obj, self.demo_id)
        self.state_population.demographics_id = self.demo_id
        self.error_band_dict = {'min_divisor': 32, 'max_divisor': 8, 'random_adjustment_points_lo': -10, 'random_adjustment_points_hi': 25}

        self.output_config_yaml = os.path.join(__location__, '..', 'datafiles', 'configs', 'utest_datagen_config.yaml')

    def tearDown(self):
        shutil.rmtree(self.output_dir)

    def test_generate_data_from_config_file(self):
        config_module = DummyClass()
        config_module.get_demograph_file = lambda *x: self.csv_file
        config_module.get_school_types = get_school_types
        config_module.get_district_types = get_district_types
        config_module.get_state_types = get_state_types
        config_module.get_states = lambda *x: [{'name': 'Example State', 'state_code': 'ES', 'state_type': 'typical_1'}]
        config_module.get_scores = lambda *x: {'min': 1200, 'max': 2400, 'cut_points': [1400, 1800, 2100], 'claim_cut_points': [1600, 2000]}
        config_module.get_temporal_information = lambda *x: {'from_date': '20120901', 'to_date': None, 'most_recent': True, 'date_taken_year': '2015', 'date_taken_month': ''}
        config_module.get_error_band = lambda *x: self.error_band_dict
        conf_output_dict = gd2.read_datagen_output_format_yaml(self.output_config_yaml)
        output_dict = initialize_csv_file(conf_output_dict, self.output_dir)

        self.assertTrue(gd2.generate_data_from_config_file(config_module, output_dict, conf_output_dict))
        #self.remove_files(list(self.ts_cvs_names.values()))

    def test_output_generated_data_to_csv(self):
        pass

    def test_get_values_from_config(self):
        config_module = DummyClass()
        config_module.get_demograph_file = lambda *x: self.csv_file
        config_module.get_school_types = get_school_types
        config_module.get_district_types = get_district_types
        config_module.get_state_types = get_state_types
        config_module.get_states = lambda *x: [{'name': 'Example State', 'state_code': 'ES', 'state_type': 'typical_1'}]
        config_module.get_scores = lambda *x: {'min': 1200, 'max': 2400, 'cut_points': [1400, 1800, 2100]}
        config_module.get_temporal_information = lambda *x: {'from_date': '20120901', 'to_date': None, 'most_recent': True, 'date_taken_year': '2015', 'date_taken_month': ''}
        config_module.get_error_band = lambda *x: self.error_band_dict

        results = gd2.get_values_from_config(config_module)
        (demographics_info, district_names, school_names, street_names, states, state_types,
         district_types, school_types, scores_details, from_date, to_date, most_recent, error_band_dict) = results

        self.assertIsInstance(demographics_info, dmg.Demographics)
        self.assertIsInstance(district_names, tuple)
        self.assertIsInstance(district_names[0], list)
        self.assertIsInstance(district_names[1], list)
        self.assertEqual(len(district_names), 2)
        self.assertIsInstance(school_names, tuple)
        self.assertIsInstance(school_names[0], list)
        self.assertIsInstance(school_names[1], list)
        self.assertEqual(len(school_names), 2)
        self.assertIsInstance(street_names, list)
        self.assertEqual(states, [{'name': 'Example State', 'state_code': 'ES', 'state_type': 'typical_1'}])
        self.assertEqual(state_types, get_state_types())
        self.assertEqual(district_types, get_district_types())
        self.assertEqual(school_types, get_school_types())
        self.assertEqual(scores_details, config_module.get_scores())
        self.assertEqual(from_date, '20120901')
        self.assertIsNone(to_date)
        self.assertTrue(most_recent)
        self.assertDictEqual(error_band_dict, self.error_band_dict)

    def test_generate_state_populations(self):
        states = [{'name': 'Example State', 'state_code': 'ES', 'state_type': 'typical_1'},
                  {'name': 'Example State 2', 'state_code': 'E2', 'state_type': 'typical_1'}]
        assessments = generate_assessments([11], [1400, 1800, 2100], [1600, 2000], date.today(), True)
        district_names = ['n{0}'.format(i) for i in range(30)]
        school_names = ['s{0}'.format(i) for i in range(30)]
        from_date = date.today()
        most_recent = True
        to_date = date(2015, 12, 12)

        results = gd2.generate_state_populations(states, get_state_types(), self.demo_obj, assessments, get_district_types(),
                                                 get_school_types(), district_names, school_names, self.error_band_dict, from_date, most_recent,
                                                 to_date, True)

        self.assertEqual(len(results), 2)
        for state_pop in results:
            self.assertIsInstance(state_pop, sp.StatePopulation)
            self.assertIsNotNone(state_pop.subject_percentages)
            self.assertEqual(len(state_pop.districts), 3)
            self.assertEqual(state_pop.state_demographic_totals[11]['all'][1], 3 * 10 * 100, '3 districts, each with 10 schools. Each school has 100 students in grade 11')

    def test_get_district_chunk(self):
        state_population = self.state_population
        chunk_size = 2
        start_pos = 0

        expected_all_students = state_population.districts[0].district_demographic_totals[11]['all'][1] +\
            state_population.districts[1].district_demographic_totals[11]['all'][1]
        result = gd2.get_district_chunk(state_population, chunk_size, start_pos)
        self.assertEqual(len(result.districts), 2)
        print('expected_all_students', expected_all_students)
        self.assertEqual(expected_all_students, result.state_demographic_totals[11]['all'][1])

    def test_get_district_chunk_2(self):
        state_population = self.state_population
        chunk_size = 2
        start_pos = 2

        result = gd2.get_district_chunk(state_population, chunk_size, start_pos)
        self.assertEqual(len(result.districts), 1)

    def test_create_state_population_from_districts(self):
        state_population = self.state_population
        district_list = [state_population.districts[0]]

        result = gd2.create_state_population_from_districts(district_list, state_population)
        self.assertDictEqual(result.state_demographic_totals, state_population.districts[0].district_demographic_totals)
        self.assertIsNot(state_population, result)
        self.assertListEqual(result.districts, district_list)

    def test_generate_districts_for_state_population_chunk(self):
        state_populations_chunk = self.state_population
        state_populations_chunk.subject_percentages = {'Math': .99, 'ELA': .99}
        assessments = generate_assessments([11], [1400, 1800, 2100], [1600, 2000], date.today(), True)
        eb_dict = self.error_band_dict
        district_names = ['n{0}'.format(i) for i in range(30)]
        school_names = ['s{0}'.format(i) for i in range(30)]
        street_names = ['st{0}'.format(i) for i in range(30)]
        from_date = date.today()
        most_recent = True
        to_date = date(2015, 12, 12)

        results = gd2.generate_districts_for_state_population_chunk(state_populations_chunk, assessments, eb_dict, district_names,
                                                                    school_names, self.demo_obj, from_date, most_recent, to_date, street_names)

        self.assertEqual(len(results), 3)

    def test_generate_districts_for_state_population_chunk_2(self):
        state_populations_chunk = self.state_population
        state_populations_chunk.districts = state_populations_chunk.districts[0:2]
        state_populations_chunk.subject_percentages = {'Math': .99, 'ELA': .99}
        assessments = generate_assessments([11], [1400, 1800, 2100], [1600, 2000], date.today(), True)
        eb_dict = self.error_band_dict
        district_names = ['n{0}'.format(i) for i in range(30)]
        school_names = ['s{0}'.format(i) for i in range(30)]
        street_names = ['st{0}'.format(i) for i in range(30)]
        from_date = date.today()
        most_recent = True
        to_date = date(2015, 12, 12)

        results = gd2.generate_districts_for_state_population_chunk(state_populations_chunk, assessments, eb_dict, district_names,
                                                                    school_names, self.demo_obj, from_date, most_recent, to_date, street_names)

        self.assertEqual(len(results), 2)

    def test_create_state_level_staff(self):
        state = DummyClass(name='Example', state_code='ES', staff=None)
        from_date = date.today()
        most_recent = True
        to_date = date(2015, 12, 12)
        staff_count = 25

        results = gd2.create_state_level_staff(state, from_date, most_recent, to_date, staff_count)
        self.assertEqual(len(results.staff), 25)

    def test_get_school_population(self):
        school_pop = sp.SchoolPopulation('High School', 'High School')
        school_pop.generate_student_numbers(get_school_types()['High School'])
        school_pop.determine_school_demographic_numbers(self.demo_obj, self.demo_id)
        school_names = ['s{0}'.format(i) for i in range(30)]
        street_names = ['st{0}'.format(i) for i in range(30)]

        subject_percentages = {'Math': .99, 'ELA': .99}
        school_grade_counts = {11: [round(x) for x in school_pop.school_demographics[11]['all'][1:]]}
        school = generate_school('High School', school_names, school_names, school_grade_counts, 'dist1', 'dguid')
        assessments = generate_assessments([11], [1400, 1800, 2100], [1600, 2000], date.today(), True)

        student_info_dict = gd2.generate_students_info_from_demographic_counts(self.state_population, assessments, self.error_band_dict)
        result = gd2.get_school_population(school, student_info_dict, subject_percentages, self.demo_obj, self.demo_id,
                                           assessments, self.error_band_dict, 'Test', 'TS',
                                           date.today(), True, None, street_names, 0)
        res_students, res_teachers, res_sections = result
        self.assertEqual(len(res_sections), 2)
        self.assertEqual(len(res_teachers), 2)
        self.assertEqual(len(res_students), 100)

    def test_get_school_population_2(self):
        school_pop = sp.SchoolPopulation('High School', 'High School')
        school_pop.generate_student_numbers(get_school_types()['High School'])
        school_pop.determine_school_demographic_numbers(self.demo_obj, self.demo_id)
        school_names = ['s{0}'.format(i) for i in range(30)]
        street_names = ['st{0}'.format(i) for i in range(30)]

        subject_percentages = {'Math': .99, 'ELA': .99}
        school_grade_counts = {11: [round(x) for x in school_pop.school_demographics[11]['all'][1:]]}
        school = generate_school('High School', school_names, school_names, school_grade_counts, 'dist1', 'dguid')
        assessments = generate_assessments([11], [1400, 1800, 2100], [1600, 2000], date.today(), True)

        student_info_dict = gd2.generate_students_info_from_demographic_counts(self.state_population, assessments, self.error_band_dict)
        result = gd2.get_school_population(school, student_info_dict, subject_percentages, self.demo_obj, self.demo_id,
                                           assessments, self.error_band_dict, 'Test', 'TS',
                                           date.today(), True, None, street_names, 0)
        res_students, res_teachers, res_sections = result

        teacher_guids = [t.staff_guid for t in res_teachers]
        section_guids = [s.section_guid for s in res_sections]
        section_rec_ids = [s.section_rec_id for s in res_sections]
        math_count, ela_count = 0, 0
        for student in res_students:
            if student.asmt_scores.get('Math'):
                math_count += 1
                self.assertIsNotNone(student.asmt_dates_taken.get('Math'))
                self.assertIn(student.teacher_guids['Math'], teacher_guids)
                self.assertIn(student.section_guids['Math'], section_guids)
                self.assertIn(student.section_rec_ids['Math'], section_rec_ids)

            if student.asmt_scores.get('ELA'):
                ela_count += 1
                self.assertIsNotNone(student.asmt_dates_taken.get('ELA'))
                self.assertIn(student.teacher_guids['ELA'], teacher_guids)
                self.assertIn(student.section_guids['ELA'], section_guids)
                self.assertIn(student.section_rec_ids['ELA'], section_rec_ids)

            self.assertIsNotNone(student.school_guid)
            self.assertIsNotNone(student.state_code)
            self.assertIsNotNone(student.district_guid)
            self.assertIsNotNone(student.from_date)
            self.assertIsNotNone(student.most_recent)

        self.assertEqual(math_count, 99, 'Check that 99% took this subject')
        self.assertEqual(ela_count, 99, 'Check that 99% took this subject')

    def test_generate_teachers_for_sections(self):
        school = DummyClass(school_guid='s1', district_guid='d1', school_name='school1')
        sections = [DummyClass(section_guid='sec1'), DummyClass(section_guid='sec2')]
        from_date = date.today()
        most_recent = True
        to_date = date(2015, 12, 12)
        state_code = 'TS'
        staff_per_section = 10

        result = gd2.generate_teachers_for_sections(staff_per_section, sections, from_date, most_recent, to_date, school, state_code)
        sec_count = Counter()
        self.assertEqual(len(result), 20)
        for staff in result:
            self.assertIsInstance(staff, Staff)
            sec_count[staff.section_guid] += 1
        self.assertEqual(sec_count['sec1'], 10)
        self.assertEqual(sec_count['sec2'], 10)

    def test_set_student_institution_information(self):
        students = [DummyClass(first_name='fname{0}'.format(i), last_name='lname{0}'.format(i))
                    for i in range(20)]
        school = DummyClass(school_guid='s1', district_guid='d1', school_name='school1')
        from_date = date.today()
        most_recent = True
        street_names = ['snames{0}'.format(i) for i in range(25)]
        state_code = 'TS'
        math_teacher = DummyClass(staff_guid='m1')
        ela_teacher = DummyClass(staff_guid='e1')
        expected_teacher_guids = {'Math': 'm1', 'ELA': 'e1'}
        to_date = date(2015, 12, 12)

        result = gd2.set_student_institution_information(students, school, from_date, most_recent, to_date, street_names, math_teacher, ela_teacher, state_code)

        for student in result:
            self.assertEqual(len(student.student_rec_ids), 2)
            self.assertIsNotNone(student.school_guid)
            self.assertIsNotNone(student.district_guid)
            self.assertIsNotNone(student.state_code)
            self.assertIsNotNone(student.school_guid)
            self.assertIsNotNone(student.district_guid)
            self.assertIsNotNone(student.state_code)
            self.assertIsNotNone(student.from_date)
            self.assertIsNotNone(student.most_recent)
            self.assertIsNotNone(student.to_date)
            self.assertIsNotNone(student.email)
            self.assertIsNotNone(student.address_1)

            self.assertDictEqual(student.teacher_guids, expected_teacher_guids)
            student_cities = student.city.split()
            self.assertEqual(len(student_cities), 2)
            self.assertIn('sname', student_cities[0])
            self.assertIn('sname', student_cities[1])

    def test_assign_students_sections(self):
        students = [DummyClass(section_rec_ids={}, section_guids={}) for _x in range(100)]
        math_sections = [DummyClass(section_guid='mg10', section_rec_id='mr10')]
        ela_sections = [DummyClass(section_guid='eg10', section_rec_id='er10')]
        expected_guid = {'Math': 'mg10', 'ELA': 'eg10'}
        expected_rec = {'Math': 'mr10', 'ELA': 'er10'}

        result = gd2.assign_students_sections(students, math_sections, ela_sections)

        for student in result:
            self.assertDictEqual(student.section_rec_ids, expected_rec)
            self.assertDictEqual(student.section_guids, expected_guid)

    def test_assign_students_sections_2(self):
        students = [DummyClass(section_rec_ids={}, section_guids={}) for _x in range(100)]
        math_sections = [DummyClass(section_guid='mg{0}'.format(i),
                                    section_rec_id='mr{0}'.format(i)) for i in range(10)]
        ela_sections = [DummyClass(section_guid='eg{0}'.format(i), section_rec_id='er{0}'.format(i))
                        for i in range(10)]
        section_guid_count = Counter()
        section_rec_count = Counter()

        result = gd2.assign_students_sections(students, math_sections, ela_sections)

        for student in result:
            section_rec_count[student.section_rec_ids['Math']] += 1
            section_rec_count[student.section_rec_ids['ELA']] += 1
            section_guid_count[student.section_guids['Math']] += 1
            section_guid_count[student.section_guids['ELA']] += 1

        self.assertEqual(len(section_rec_count), 20, '10 math, 10 ela')
        self.assertEqual(len(section_guid_count), 20, '10 math, 10 ela')
        for guid in section_guid_count:
            self.assertEqual(section_guid_count[guid], 10, 'Each section should have 10 students')
        for rec_id in section_rec_count:
            self.assertEqual(section_rec_count[rec_id], 10, 'Each section should have 10 students')

    def test_set_students_asmt_info(self):
        students = [DummyClass(asmt_rec_ids={}, asmt_guids={}, asmt_dates_taken={}, asmt_years={}, asmt_types={}, asmt_subjects={}) for _x in range(100)]
        subjects = ['Math', 'ELA']
        asmt_rec_ids = ['123', '456']
        asmt_guids = ['ag123', 'ag123r4']
        dates_taken = [date(2013, 12, 2), date(2001, 11, 5)]
        asmt_types = ['SUMMATIVE', 'SUMMATIVE']
        asmt_years = [2015, 1920]
        expected_asmt_rec_ids = {'Math': '123', 'ELA': '456'}
        expected_asmt_guids = {'Math': 'ag123', 'ELA': 'ag123r4'}
        expected_dates_taken = {'Math': date(2013, 12, 2), 'ELA': date(2001, 11, 5)}
        expected_asmt_types = {'Math': 'SUMMATIVE', 'ELA': 'SUMMATIVE'}
        expected_asmt_years = {'Math': 2015, 'ELA': 1920}
        expected_asmt_subjects = {'Math': 'Math', 'ELA': 'ELA'}

        result = gd2.set_students_asmt_info(students, subjects, asmt_rec_ids, asmt_guids, dates_taken, asmt_years, asmt_types)

        for student in result:
            self.assertDictEqual(student.asmt_rec_ids, expected_asmt_rec_ids)
            self.assertDictEqual(student.asmt_guids, expected_asmt_guids)
            self.assertDictEqual(student.asmt_dates_taken, expected_dates_taken)
            self.assertDictEqual(student.asmt_years, expected_asmt_years)
            self.assertDictEqual(student.asmt_types, expected_asmt_types)
            self.assertDictEqual(student.asmt_subjects, expected_asmt_subjects)

    def test_apply_subject_percentages(self):
        students = [DummyClass(asmt_scores={'Math': 'score', 'ELA': 'score'}) for _i in range(100)]
        subject_percentages = {'Math': .75, 'ELA': .75}
        result = gd2.apply_subject_percentages(subject_percentages, students)

        math_count, ela_count = 0, 0
        for student in result:
            if student.asmt_scores.get('Math'):
                math_count += 1
            if student.asmt_scores.get('ELA'):
                ela_count += 1
        self.assertEqual(math_count, 75)
        self.assertEqual(ela_count, 75)

    def test_apply_subject_percentages_2(self):
        students = [DummyClass(asmt_scores={'Math': 'score', 'ELA': 'score'}) for _i in range(100)]
        subject_percentages = {'Math': .80, 'ELA': .95}
        gd2.apply_subject_percentages(subject_percentages, students)

        math_count, ela_count = 0, 0
        for student in students:
            if student.asmt_scores.get('Math'):
                math_count += 1
            if student.asmt_scores.get('ELA'):
                ela_count += 1
        self.assertEqual(math_count, 80)
        self.assertEqual(ela_count, 95)

    def test_get_students_by_counts(self):
        grade = 11
        grade_counts = [100, 35, 40, 15, 10]
        student_info_dict = {grade: {1: [DummyClass(pl=1) for _x in range(35)], 2: [DummyClass(pl=2) for _x in range(40)],
                                     3: [DummyClass(pl=3) for _x in range(15)], 4: [DummyClass(pl=4) for _x in range(10)]}}
        results = gd2.get_students_by_counts(grade, grade_counts, student_info_dict)
        self.assertEqual(len(results), 100)
        counts = [100, 0, 0, 0, 0]
        for student in results:
            counts[student.pl] += 1

        self.assertListEqual(counts, grade_counts)

    def test_get_students_by_counts_2(self):
        grade = 11
        grade_counts = [100, 35, 40, 15, 10]
        student_info_dict = {grade: {1: [DummyClass(pl=1) for _x in range(35)], 2: [DummyClass(pl=2) for _x in range(35)],
                                     3: [DummyClass(pl=3) for _x in range(15)], 4: [DummyClass(pl=4) for _x in range(10)]}}
        results = gd2.get_students_by_counts(grade, grade_counts, student_info_dict)
        self.assertEqual(len(results), 95)
        expected_counts = [100, 35, 35, 15, 10]
        counts = [100, 0, 0, 0, 0]
        for student in results:
            counts[student.pl] += 1

        self.assertListEqual(counts, expected_counts)

    def test_create_schools(self):
        district_pop = sp.DistrictPopulation('Big Average')
        district_pop.populate_district(get_district_types()['Big Average'], get_school_types())
        district_pop.determine_district_demographics(self.demo_obj, self.demo_id)

        school_names = ['s{0}'.format(i) for i in range(30)]
        street_names = ['st{0}'.format(i) for i in range(30)]
        district = he.District('guid1', 'District9', 'Big Average', district_pop.schools)
        subject_percentages = {'Math': .99, 'ELA': .99}
        assessments = generate_assessments([3, 4, 5, 6, 7, 8, 11], [1400, 1800, 2100], [1600, 2000], date.today(), True)
        student_info_dict = gd2.generate_students_info_from_demographic_counts(self.state_population, assessments, self.error_band_dict)

        result = gd2.create_schools(district, school_names, school_names, student_info_dict, subject_percentages,
                                    self.demo_obj, self.demo_id, assessments, self.error_band_dict, 'Test', 'TS',
                                    date.today(), True, None, street_names)

        self.assertEqual(len(result), len(district_pop.schools))
        for school in result:
            self.assertIsNotNone(school.student_info)
            self.assertIsInstance(school.student_info, list)
            self.assertGreater(len(school.student_info), 0)
            self.assertIsNotNone(school.teachers)
            self.assertIsInstance(school.teachers, list)
            self.assertGreater(len(school.teachers), 0)
            self.assertIsNotNone(school.sections)
            self.assertIsInstance(school.sections, list)
            self.assertGreater(len(school.sections), 0)

    def test_create_districts(self):
        district_names = ['n{0}'.format(i) for i in range(30)]
        school_names = ['s{0}'.format(i) for i in range(30)]
        street_names = ['st{0}'.format(i) for i in range(30)]
        subject_percentages = {'Math': .99, 'ELA': .99}
        assessments = generate_assessments([3, 4, 5, 6, 7, 8, 11], [1400, 1800, 2100], [1600, 2000], date.today(), True)
        student_info_dict = gd2.generate_students_info_from_demographic_counts(self.state_population, assessments, self.error_band_dict)

        results = gd2.create_districts(self.state_population, district_names, district_names, school_names, school_names,
                                       student_info_dict, subject_percentages, self.demo_obj, self.demo_id, assessments,
                                       self.error_band_dict, "Test", 'TS', date.today(), True, None, street_names)

        # taken from state_types dict
        expected_district_count = 3
        self.assertEqual(len(results), expected_district_count)
        for district in results:
            self.assertEqual(len(district.staff), 10)
            self.assertEqual(len(district.schools), 10)

    def test_generate_students_info_from_demographic_counts_overall_counts(self):
        state_pop = DummyClass()
        state_pop.subject = 'math'
        grade = 3
        state_pop.state_demographic_totals = {3: {'all': [0, 72, 18, 18, 18, 18],
                                                  'male': [1, 20, 5, 5, 5, 5],
                                                  'female': [1, 24, 6, 6, 6, 6],
                                                  'not_stated': [1, 28, 7, 7, 7, 7],
                                                  'dmg_eth_ami': [2, 48, 12, 12, 12, 12],
                                                  'dmg_eth_blk': [2, 24, 6, 6, 6, 6]}
                                              }
        assessments = generate_assessments([grade], [1400, 1800, 2100], [1600, 2000], date.today(), True)

        result = gd2.generate_students_info_from_demographic_counts(state_pop, assessments, self.error_band_dict)

        self.assertEqual(len(result[grade][1]), 18)
        self.assertEqual(len(result[grade][2]), 18)
        self.assertEqual(len(result[grade][3]), 18)
        self.assertEqual(len(result[grade][4]), 18)

    def test_generate_students_info_from_demographic_counts_counts(self):
        state_pop = DummyClass()
        state_pop.subject = 'math'
        grade = 3
        state_pop.state_demographic_totals = {3: {'all': [0, 72, 18, 18, 18, 18],
                                                  'male': [1, 20, 5, 5, 5, 5],
                                                  'female': [1, 24, 6, 6, 6, 6],
                                                  'not_stated': [1, 28, 7, 7, 7, 7],
                                                  'dmg_eth_ami': [2, 48, 12, 12, 12, 12],
                                                  'dmg_eth_blk': [2, 24, 5.5, 5.2, 6, 6]}
                                              }
        assessments = generate_assessments([grade], [1400, 1800, 2100], [1600, 2000], date.today(), True)

        result = gd2.generate_students_info_from_demographic_counts(state_pop, assessments, self.error_band_dict)

        self.assertEqual(len(result[grade]), 4)
        for pl in result[grade]:
            counts = {'male': 0, 'female': 0, 'not_stated': 0, 'dmg_eth_ami': 0, 'dmg_eth_blk': 0}
            expected_counts = {'male': 5, 'female': 6, 'not_stated': 7, 'dmg_eth_ami': 12, 'dmg_eth_blk': 6}
            for student in result[grade][pl]:
                demographs = student.getDemoOfStudent()
                for demo in demographs:
                    counts[demo] += 1
            self.assertDictEqual(counts, expected_counts)

    def test_generate_students_with_demographics(self):
        score_pool = {1: [x for x in range(100)], 2: [x for x in range(100)],
                      3: [x for x in range(100)], 4: [x for x in range(100)]}
        demographic_totals = {'male': [1, 20, 5, 5, 5, 5],
                              'female': [1, 24, 6, 6, 6, 6],
                              'not_stated': [1, 28, 7, 7, 7, 7],
                              'dmg_eth_ami': [2, 28, 7, 7, 7, 7],
                              'dmg_eth_blk': [2, 24, 6, 6, 6, 6]}
        grade = 3
        results = gd2.generate_students_with_demographics(score_pool, demographic_totals, grade)
        self.assertEquals(len(results), 4)

    def test_assign_demographics_for_grouping(self):
        group_num = 1
        student_info_pool = {1: [he.StudentInfo(3, 'male', 12) for _i in range(50)],
                             2: [he.StudentInfo(3, 'male', 12) for _i in range(50)],
                             3: [he.StudentInfo(3, 'male', 12) for _i in range(50)],
                             4: [he.StudentInfo(3, 'male', 12) for _i in range(50)]}
        demographic_totals = {'dmg_eth_wht': [1, 20, 5, 5, 5, 5], 'dmg_eth_blk': [1, 24, 6, 6, 6, 6], 'dmg_eth_asn': [1, 28, 7, 7, 7, 7]}

        gd2.assign_demographics_for_grouping(group_num, student_info_pool, demographic_totals)
        bcounts = {1: 0, 2: 0, 3: 0, 4: 0}
        acounts = {1: 0, 2: 0, 3: 0, 4: 0}
        wcounts = {1: 0, 2: 0, 3: 0, 4: 0}
        for perf_lvl, stud_list in student_info_pool.items():
            self.assertEqual(len(stud_list), 50)
            for stu in stud_list:
                if stu.dmg_eth_wht is True:
                    wcounts[perf_lvl] += 1
                if stu.dmg_eth_blk is True:
                    bcounts[perf_lvl] += 1
                if stu.dmg_eth_asn is True:
                    acounts[perf_lvl] += 1

        self.assertEqual(bcounts[1], 6)
        self.assertEqual(acounts[2], 7)
        self.assertEqual(wcounts[3], 5)
        self.assertEqual(wcounts[4], 5)

    def test_assign_demographic_to_students(self):
        demographic_name = 'dem1'
        perf_lvl_lst = [he.StudentInfo(3, 'female', 12)] * 10
        student_pool = {1: [he.StudentInfo(3, 'male', 12)] * 10,
                        2: perf_lvl_lst[:],
                        3: [he.StudentInfo(3, 'male', 12)] * 10,
                        4: [he.StudentInfo(3, 'female', 12)] * 10}
        count = 10
        performance_level = 2

        gd2.assign_demographic_to_students(demographic_name, student_pool, count, performance_level)
        print(perf_lvl_lst)
        self.assertEqual(len(perf_lvl_lst), 10)
        for stud_info in perf_lvl_lst:
            self.assertTrue(stud_info.dem1)

    def test_assign_demographic_to_students_2(self):
        demographic_name = 'dmg_prg_tt1'
        perf_lvl_lst_1 = [he.StudentInfo(3, 'male', 12) for _i in range(10)]
        perf_lvl_lst_2 = [he.StudentInfo(3, 'female', 12) for _i in range(10)]
        perf_lvl_lst_3 = [he.StudentInfo(3, 'male', 12) for _i in range(10)]
        perf_lvl_lst_4 = [he.StudentInfo(3, 'female', 12) for _i in range(10)]

        student_pool = {1: perf_lvl_lst_1[:],
                        2: perf_lvl_lst_2[:],
                        3: perf_lvl_lst_3[:],
                        4: perf_lvl_lst_4[:]}
        count = 5
        performance_level = 1

        gd2.assign_demographic_to_students(demographic_name, student_pool, count, performance_level)

        num_true = 0
        print(perf_lvl_lst_1)
        self.assertEqual(len(perf_lvl_lst_1), 10)
        for stud_info in perf_lvl_lst_1:
            if stud_info.dmg_prg_tt1 is True:
                num_true += 1

        self.assertEqual(num_true, 5)

    def test_create_student_info_dict(self):
        group_num = 1
        score_pool = {1: [x for x in range(100)], 2: [x for x in range(100)],
                      3: [x for x in range(100)], 4: [x for x in range(100)]}
        demographic_totals = {'male': [1, 20, 5, 5, 5, 5], 'female': [1, 24, 6, 6, 6, 6], 'not_stated': [1, 28, 7, 7, 7, 7]}
        grade = 3
        result = gd2.create_student_info_dict(group_num, score_pool, demographic_totals, grade)

        for perf_lvl in result:
            self.assertEqual(len(result[perf_lvl]), 18)

    def test_create_student_infos_by_gender(self):
        gender = 'male'
        count = 30
        performance_level = 1
        score_pool = {1: [x for x in range(count)]}
        grade = 3
        studentInfo_list = gd2.create_student_infos_by_gender(gender, count, performance_level, score_pool, grade)
        self.assertEqual(len(studentInfo_list), count)
        print(studentInfo_list[0].asmt_scores)

    def test_create_asmt_score_pool_dict(self):
        total = 100
        perf_lvls = 4
        pl_size = total / perf_lvls
        asmt_scores = [DummyClass() for _x in range(total)]
        for i in range(len(asmt_scores)):
            asmt_scores[i].perf_lvl = (i % perf_lvls) + 1

        result = gd2.create_asmt_score_pool_dict(asmt_scores)
        self.assertEqual(len(result), perf_lvls)

        # Check all performance levels have 25 scores
        [self.assertEqual(len(result[pl]), pl_size) for pl in result]

    def test_generate_name_list_dictionary(self):
        list_name_to_path_dictionary = {}
        file_count = 10
        name_count = 50
        file_names = self.create_mock_name_files(file_count, name_count)
        for name in file_names:
            list_name_to_path_dictionary[name] = name
        res = gd2.generate_name_list_dictionary(list_name_to_path_dictionary)

        self.assertEqual(len(res), file_count)
        for name in res:
            number_of_lines = len(res[name])
            self.assertEqual(number_of_lines, name_count)
        #self.remove_files(file_names)

    def test_get_flat_grades_list(self):
        school_config = {
            'High School': {'grades': [11], 'students': {'min': 100, 'max': 500, 'avg': 300}},
            'Jr. High School': {'grades': [9, 10, 11], 'students': {'min': 100, 'max': 500, 'avg': 300}},
            'Middle School': {'grades': [6, 7, 8], 'students': {'min': 50, 'max': 200, 'avg': 150}},
            'Elementary School': {'grades': [1, 3, 4, 5], 'students': {'min': 20, 'max': 70, 'avg': 60}}
        }
        expected_items = [11, 9, 10, 6, 7, 8, 1, 3, 4, 5]
        res = gd2.get_flat_grades_list(school_config, 'grades')
        self.assertEqual(len(res), len(expected_items))
        for it in expected_items:
            self.assertIn(it, res)
        diffs = set(expected_items) ^ set(res)
        self.assertFalse(diffs)

    def test_generate_non_teaching_staff(self):
        state_code = 'GA'
        num_of_staff = 20
        district_guid = 'distguid'
        school_guid = 'schoolguid'
        res = gd2.generate_non_teaching_staff(num_of_staff, self.from_date, self.most_recent, self.to_date,
                                              state_code, district_guid, school_guid)
        self.assertEqual(len(res), num_of_staff)
        for staff in res:
            self.assertIsInstance(staff, Staff)
            self.assertEqual(staff.hier_user_type, 'Staff')
            self.assertEqual(staff.to_date, self.to_date)
            self.assertEqual(staff.from_date, self.from_date)
            self.assertEqual(staff.most_recent, self.most_recent)
            self.assertEqual(staff.state_code, state_code)
            self.assertEqual(staff.district_guid, district_guid)
            self.assertEqual(staff.school_guid, school_guid)

    def test_generate_institution_hierarchy_from_helper_entities(self):
        state_population = DummyClass()
        state_population.state_name = 'Georgia'
        state_population.state_code = 'GA'
        district = DummyClass()
        district.district_guid = 'dguid1'
        district.district_name = 'District1'
        school = DummyClass()
        school.school_name = 'School1'
        school.school_guid = 'sguid1'
        school.school_category = 'Middle'

        res = gd2.generate_institution_hierarchy_from_helper_entities(state_population, district, school, self.from_date,
                                                                      self.most_recent, self.to_date)

        self.assertIsInstance(res, InstitutionHierarchy)
        self.assertEqual(res.state_name, 'Georgia')
        self.assertEqual(res.state_code, 'GA')
        self.assertEqual(res.district_name, 'District1')
        self.assertEqual(res.school_name, 'School1')
        self.assertEqual(res.school_category, 'Middle')

    def test_create_output_dict(self):
        gd2.CSV_FILE_NAMES = self.csv_file_names
        result = gd2.create_output_dict(self.output_dir)

        self.assertDictEqual(result, self.entity_to_path_dict)

    ##==================================
    ## Helper Methods
    ##==================================
    def read_row_in_csv(self, file_name, row):
        with open(file_name, 'r') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)
            self.assertListEqual(header, row)

    def create_mock_name_files(self, file_count, name_count):
        list_name = 'unit_test_file_for_testing{num}'
        file_list = []
        for i in range(file_count):
            file_name = os.path.join(self.output_dir, list_name.format(num=i))
            with open(file_name, 'w') as f:
                for i in range(name_count):
                    f.write('name_{0}\n'.format(i))
            file_list.append(file_name)
        return file_list

    def remove_files(self, file_list):
        for name in file_list:
            os.remove(name)


class DummyClass:
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])


class DummyEntity1(object):
    def __init__(self):
        pass

    @classmethod
    def getHeader(self):
        return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']


class DummyEntity2(object):
    def __init__(self):
        pass

    @classmethod
    def getHeader(self):
        return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']


def write_demographics_csv(output_dir):
    csv_file_data = [
        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '3', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '3', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '3', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '3', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '3', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '3', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '3', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '3', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '3', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '3', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '3', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '11', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '11', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '11', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '11', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '11', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '11', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '11', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '11', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '11', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '11', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '11', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'ela', '11', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'ela', '11', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'ela', '11', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'ela', '11', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'ela', '11', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'ela', '11', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'ela', '11', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'ela', '11', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'ela', '11', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'ela', '11', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'ela', '11', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),
    ]

    file_path = os.path.join(output_dir, 'test_file.csv')

    with open(file_path, 'w') as cfile:
        cwriter = csv.writer(cfile)
        for row in csv_file_data:
            cwriter.writerow(row)

    return file_path


def get_district_types():
    district_types = {'Big Average': {'school_counts': {'min': 10, 'max': 10, 'avg': 10},
                                      'school_types_and_ratios': {
                                          'High School': 1}}}  # , 'Middle School': 1, 'Elementary School': 1}}}
    return district_types


def get_school_types():
    school_types = {
        'High School': {'type': 'High School', 'grades': [11], 'students': {'min': 100, 'max': 100, 'avg': 100}},
        'Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 100, 'max': 100, 'avg': 100}},
        'Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 100, 'max': 100, 'avg': 100}}}

    return school_types


def get_state_types():
    state_types = {'typical_1': {'district_types_and_counts': {'Big Average': 3},
                                 'subjects_and_percentages': {'Math': .99, 'ELA': .99},
                                 'demographics': 'typical1'}
                   }
    return state_types


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
