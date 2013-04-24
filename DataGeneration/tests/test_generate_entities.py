import unittest
import constants as constants
from datetime import date
from uuid import UUID, uuid4
from generate_entities import generate_institution_hierarchy, generate_student, generate_section, generate_staff, \
    generate_assessment, generate_students, generate_sections, generate_assessments, generate_multiple_staff, \
    generate_fact_assessment_outcome, generate_fact_assessment_outcomes
from entities import Student, Section, Assessment, Staff, AssessmentOutcome
from helper_entities import AssessmentScore, ClaimScore

class TestGenerateEntities(unittest.TestCase):

    def test_generate_institution_hierarchy(self):
        params = {
            'state_name': 'New York',
            'state_code': 'NY',
            'district_guid': 1,
            'district_name': 'district_1',
            'school_guid': 2,
            'school_name': 'school_2',
            'school_category': 'High School',
            'from_date':  date(2013, 4, 15),
            'most_recent':  True
        }
        institution_hierarchy = generate_institution_hierarchy(**params)
        self.assertEquals(institution_hierarchy.state_name, params['state_name'])
        self.assertEquals(institution_hierarchy.state_code, params['state_code'])
        self.assertEquals(institution_hierarchy.district_guid, params['district_guid'])
        self.assertEquals(institution_hierarchy.district_name, params['district_name'])
        self.assertEquals(institution_hierarchy.school_guid, params['school_guid'])
        self.assertEquals(institution_hierarchy.school_name, params['school_name'])
        self.assertEquals(institution_hierarchy.school_category, params['school_category'])
        self.assertEquals(institution_hierarchy.from_date, params['from_date'])
        self.assertEquals(institution_hierarchy.most_recent, params['most_recent'])
        self.assertIsInstance(institution_hierarchy.inst_hier_rec_id, int)

    def test_generate_student(self):
        params = {
            'section_guid': 1,
            'grade': 9,
            'state_code': 'NY',
            'district_guid': 2,
            'school_guid': 3,
            'school_name': 'school_2',
            'street_names': ['Suffolk', 'President', 'Allen'],
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        student = generate_student(**params)
        self.assertIsInstance(student.student_rec_id, int)
        self.assertIsInstance(student.student_guid, UUID)
        self.assertIsInstance(student.first_name, str)
        self.assertIsInstance(student.last_name, str)
        address_component_words = student.address_1.split()
        address= int(address_component_words[0])
        street_name = address_component_words[1]
        suffix = address_component_words[2].upper()
        self.assertIsInstance(address, int)
        self.assertIn(street_name, params['street_names'])
        self.assertIn(suffix, constants.ADD_SUFFIX)
        city_component_words = student.city.split()
        city_name_1 = city_component_words[0]
        city_name_2 = city_component_words[1]
        self.assertIn(city_name_1, params['street_names'])
        self.assertIn(city_name_2, params['street_names'])
        self.assertIsInstance(student.zip_code, int)
        self.assertIn(student.gender, constants.GENDERS)
        self.assertIsInstance(student.email, str)
        self.assertIsInstance(student.dob, str)
        self.assertEquals(student.section_guid, params['section_guid'])
        self.assertEquals(student.grade, params['grade'])
        self.assertEquals(student.state_code, params['state_code'])
        self.assertEquals(student.district_guid, params['district_guid'])
        self.assertEquals(student.school_guid, params['school_guid'])
        self.assertIsInstance(student.from_date, date)
        self.assertIsInstance(student.most_recent, bool)

    def test_generate_students(self):
        params = {
            'number_of_students': 5,
            'section_guid': uuid4(),
            'grade': 5,
            'state_code': 'NY',
            'district_guid': uuid4(),
            'school_guid': uuid4(),
            'school_name': 'P.S. 118',
            'street_names': ['Vine, Main, Park'],
            'from_date': date(2013, 4, 23),
            'most_recent': True
        }
        students = generate_students(**params)
        self.assertEquals(len(students), params['number_of_students'])
        for student in students:
            self.assertIsInstance(student, Student)


    def test_generate_section(self):
        params = {
            'subject_name': 'ELA',
            'grade': 9,
            'state_code': 'NY',
            'district_guid': 1,
            'school_guid': 2,
            'section_number': 1,
            'class_number': 2,
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        section = generate_section(**params)
        self.assertIsInstance(section.section_rec_id, int)
        self.assertIsInstance(section.section_guid, UUID)
        section_component_words = section.section_name.split()
        section_name = section_component_words[0]
        section_number = section_component_words[1]
        self.assertEquals(section_name, 'Section')
        self.assertEquals(int(section_number), params['section_number'])
        self.assertEquals(section.grade, params['grade'])
        class_component_words = section.class_name.split('_')
        class_name = class_component_words[0]
        class_number = int(class_component_words[1])
        self.assertEquals(class_name, params['subject_name'])
        self.assertEquals(class_number, params['class_number'])


    def test_generate_sections(self):
        params = {
            'number_of_sections': 9,
            'subject_name': 'ELA',
            'grade': 9,
            'state_code': 'NY',
            'district_guid': uuid4(),
            'school_guid': uuid4(),
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        sections = generate_sections(**params)
        self.assertEquals(len(sections), params['number_of_sections'])
        for section in sections:
            self.assertIsInstance(section, Section)


    def test_generate_assessment(self):
        params = {
            'asmt_type': 'Summative',
            'asmt_period': 'Spring',
            'asmt_period_year': 2012,
            'asmt_subject': 'Math',
            'asmt_grade': 9,
            'asmt_cut_point_1': 1400,
            'asmt_cut_point_2': 1800,
            'asmt_cut_point_3': 2100,
            'asmt_cut_point_4': 2200,
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        a = generate_assessment(**params)
        self.assertIsInstance(a.asmt_rec_id, int)
        self.assertIsInstance(a.asmt_guid, UUID)
        self.assertEquals(a.asmt_type, params['asmt_type'])


    def test_generate_assessments(self):
        params = {
            'grades': [9,10,11],
            'cut_points' : [1400, 1800, 2100],
            'from_date': date(2013,4,23),
            'most_recent': True
        }
        assessments = generate_assessments(**params)
        for assessment in assessments:
            self.assertIsInstance(assessment, Assessment)

    def test_generate_staff(self):
        params = {
            'hier_user_type': 'Staff',
            'state_code': 'NY',
            'district_guid': 1,
            'school_guid': 2,
            'section_guid': 3,
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }

        staff = generate_staff(**params)
        self.assertIsInstance(staff.staff_rec_id, int)
        self.assertIsInstance(staff.staff_guid, UUID)
        self.assertIsInstance(staff.first_name, str)
        self.assertIsInstance(staff.last_name, str)
        self.assertEquals(staff.section_guid, params['section_guid'])
        self.assertEquals(staff.hier_user_type, params['hier_user_type'])
        self.assertEquals(staff.state_code, params['state_code'])
        self.assertEquals(staff.district_guid, params['district_guid'])
        self.assertEquals(staff.school_guid, params['school_guid'])
        self.assertIsInstance(staff.from_date, date)
        self.assertIsInstance(staff.most_recent, bool)

    def test_generate_multiple_staff(self):
        params = {
            'number_of_staff': 8,
            'hier_user_type': 'Teacher',
            'state_code': 'NY',
            'district_guid': uuid4(),
            'school_guid': uuid4(),
            'section_guid': uuid4(),
            'from_date': date(2013, 4, 15),
            'most_recent': True
        }
        staff = generate_multiple_staff(**params)
        self.assertEquals(len(staff), params['number_of_staff'])
        for staff_member in staff:
            self.assertIsInstance(staff_member, Staff)


    def test_generate_fact_assessment_outcome(self):
        params = {
            'asmt_rec_id': 10,
            'student_guid': uuid4(),
            'teacher_guid': uuid4(),
            'state_code': 'NY',
            'district_guid': uuid4(),
            'school_guid': uuid4(),
            'section_guid': uuid4(),
            'inst_hier_rec_id': 9,
            'section_rec_id': 13,
            'where_taken_id': 27,
            'where_taken_name': 'P.S. 118',
            'asmt_grade': 7,
            'enrl_grade': 7,
            'date_taken': date(2013,4,23),
            'date_taken_day': 23,
            'date_taken_month': 4,
            'date_taken_year': 2013,
            'asmt_score': 1750,
            'asmt_score_range_min': 1650,
            'asmt_score_range_max': 1850,
            'asmt_perf_lvl': 1,
            'asmt_claim_1_score': 1800,
            'asmt_claim_1_score_range_min': 1700,
            'asmt_claim_1_score_range_max': 1900,
            'asmt_claim_2_score': 1600,
            'asmt_claim_2_score_range_min': 1500,
            'asmt_claim_2_score_range_max': 1700,
            'asmt_claim_3_score': 1790,
            'asmt_claim_3_score_range_min': 1690,
            'asmt_claim_3_score_range_max': 1890,
            'asmt_claim_4_score': 1729,
            'asmt_claim_4_score_range_min': 1629,
            'asmt_claim_4_score_range_max': 1829
        }
        assessment_outcome = generate_fact_assessment_outcome(**params)
        self.assertIsInstance(assessment_outcome, AssessmentOutcome)
        for key, value in params.items():
            self.assertEquals(getattr(assessment_outcome, key), value)


    def test_generate_fact_assessment_outcomes(self):
        section_guid = uuid4()
        grade = 10
        state_code = 'NY'
        district_guid = uuid4()
        school_guid = uuid4()
        from_date = date(2013, 4, 23)
        most_recent = True
        student_1 = Student(100, uuid4(), 'Seth', 'Wimberly', '55 Washington St', 'Brooklyn', 11215,
                            'Male', 'swimbery@swimberly.com', date(1988, 1, 1),
                            section_guid, grade, state_code, district_guid, school_guid, from_date, most_recent)
        student_2 = Student(100, uuid4(), 'Scott', 'MacGibbon', '65 Washington St', 'Brooklyn', 11215,
                            'Male', 'smacgibbon@smacgibbon.com', date(1988, 3, 3),
                            section_guid, grade, state_code, district_guid, school_guid, from_date, most_recent)
        students = [student_1, student_2]

        claim_score_1_a = ClaimScore(1800, 1700, 1900)
        claim_score_1_b = ClaimScore(1900, 1800, 2000)
        claim_score_1_c = ClaimScore(2000, 1900, 2100)
        claim_scores_1 = [claim_score_1_a, claim_score_1_b, claim_score_1_c]
        score_1 = AssessmentScore(1900, 3, 1800, 1900, claim_scores_1, date(2013,4,23))

        claim_score_2_a = ClaimScore(1900, 1800, 2000)
        claim_score_2_b = ClaimScore(2100, 2000, 2200)
        claim_score_2_c = ClaimScore(2000, 1900, 2100)
        claim_scores_2 = [claim_score_2_a, claim_score_2_b, claim_score_2_c]
        score_2 = AssessmentScore(2000, 3, 1900, 2100, claim_scores_2, date(2013,4,23))

        scores = [score_1, score_2]
        teacher_guid = uuid4()
        params = {
            'students': students,
            'scores': scores,
            'asmt_rec_id': 111,
            'teacher_guid': teacher_guid,
            'state_code': state_code,
            'district_guid': district_guid,
            'school_guid': school_guid,
            'section_guid': section_guid,
            'inst_hier_rec_id': 200,
            'section_rec_id': 300,
            'where_taken_id': school_guid,
            'where_taken_name': 'P.S. 118',
            'asmt_grade': 10,
            'enrl_grade': 10,
            'date_taken': date(2013, 4, 23),
            'date_taken_day': 23,
            'date_taken_month': 4,
            'date_taken_year': 2013
        }

        assessment_outcomes = generate_fact_assessment_outcomes(**params)
        self.assertEquals(len(assessment_outcomes), len(students))
        for assessment_outcome in assessment_outcomes:
            self.assertIsInstance(assessment_outcome, AssessmentOutcome)