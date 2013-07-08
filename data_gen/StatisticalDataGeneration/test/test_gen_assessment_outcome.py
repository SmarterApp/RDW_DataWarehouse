import unittest
import gen_assessment_outcome
from gen_assessments import generate_dim_assessment
from constants import ASSMT_SCORE_YEARS, MINIMUM_ASSESSMENT_SCORE, MAXIMUM_ASSESSMENT_SCORE
from helper_entities import WhereTaken
from helper_entities import StudentBioInfo, Claim, AssessmentScore
from entities import Student, AssessmentOutcome, Assessment


class TestGenAssessmentOutcome(unittest.TestCase):

    def test_generate_assessment_outcomes_from_student_object_list_three_claims(self):
        assessment_list = generate_dim_assessment()
        students = make_students_list(5)
        subject = 'Math'
        inst_hier_rec_id = 12345
        where_taken = WhereTaken(91845, 'where_taken_test_name')
        actual_assessment_outcomes = gen_assessment_outcome.generate_assessment_outcomes_from_student_object_list(assessment_list, students, subject, inst_hier_rec_id, where_taken)
        self.assertEqual(len(actual_assessment_outcomes), len(students) * len(ASSMT_SCORE_YEARS) * 4)
        for outcome in actual_assessment_outcomes:
            self.assertEqual(outcome.where_taken_id, where_taken.where_taken_id)
            self.assertEqual(outcome.where_taken_name, where_taken.where_taken_name)
            self.assertEqual(outcome.enrl_grade, students[0].grade)
            # score related
            self.assertTrue(outcome.asmt_score in range(1200, 2401))
            self.assertTrue(outcome.asmt_perf_lvl in [1, 2, 3, 4])
            self.assertTrue(10 < outcome.asmt_claim_1_score < 99)
            self.assertTrue(10 < outcome.asmt_claim_2_score < 99)
            self.assertTrue(10 < outcome.asmt_claim_3_score < 99)
            self.assertTrue(outcome.asmt_claim_1_score_range_min <= outcome.asmt_claim_1_score <= outcome.asmt_claim_1_score_range_max)
            self.assertTrue(outcome.asmt_claim_2_score_range_min <= outcome.asmt_claim_2_score <= outcome.asmt_claim_2_score_range_max)
            self.assertTrue(outcome.asmt_claim_3_score_range_min <= outcome.asmt_claim_3_score <= outcome.asmt_claim_3_score_range_max)

            # claim 4 is none
            self.assertIsNone(outcome.asmt_claim_4_score)
            self.assertIsNone(outcome.asmt_claim_4_score_range_min)
            self.assertIsNone(outcome.asmt_claim_4_score_range_max)

    def test_generate_assessment_outcomes_from_student_object_list_four_claims(self):
        assessment_list = generate_dim_assessment()
        students = make_students_list(5)
        subject = 'ELA'
        inst_hier_rec_id = 12345
        where_taken = WhereTaken(91845, 'where_taken_test_name')
        actual_assessment_outcomes = gen_assessment_outcome.generate_assessment_outcomes_from_student_object_list(assessment_list, students, subject, inst_hier_rec_id, where_taken)
        self.assertEqual(len(actual_assessment_outcomes), len(students) * len(ASSMT_SCORE_YEARS) * 4)
        for outcome in actual_assessment_outcomes:
            self.assertEqual(outcome.where_taken_id, where_taken.where_taken_id)
            self.assertEqual(outcome.where_taken_name, where_taken.where_taken_name)
            self.assertEqual(outcome.enrl_grade, students[0].grade)
            # score related
            self.assertTrue(outcome.asmt_score in range(1200, 2401))
            self.assertTrue(outcome.asmt_perf_lvl in [1, 2, 3, 4])
            self.assertTrue(10 < outcome.asmt_claim_1_score < 99)
            self.assertTrue(10 < outcome.asmt_claim_2_score < 99)
            self.assertTrue(10 < outcome.asmt_claim_3_score < 99)
            self.assertTrue(10 < outcome.asmt_claim_4_score < 99)

            self.assertTrue(outcome.asmt_claim_1_score_range_min <= outcome.asmt_claim_1_score <= outcome.asmt_claim_1_score_range_max)
            self.assertTrue(outcome.asmt_claim_2_score_range_min <= outcome.asmt_claim_2_score <= outcome.asmt_claim_2_score_range_max)
            self.assertTrue(outcome.asmt_claim_3_score_range_min <= outcome.asmt_claim_3_score <= outcome.asmt_claim_3_score_range_max)
            self.assertTrue(outcome.asmt_claim_4_score_range_min <= outcome.asmt_claim_4_score <= outcome.asmt_claim_4_score_range_max)

    def test_get_filtered_assessments_same_case_subject(self):
        subject = 'Math'
        grade = 5
        assessment_list = generate_dim_assessment()
        actual_filtered_assessments = gen_assessment_outcome.get_filtered_assessments(subject, grade, assessment_list)
        self.assertEqual(len(actual_filtered_assessments), len(ASSMT_SCORE_YEARS) * 4)
        for assessment in actual_filtered_assessments:
            self.assertEqual(assessment.asmt_grade, grade)
            self.assertEqual(assessment.asmt_subject.lower(), subject.lower())

    def test_get_filtered_assessments_different_case_subject(self):
        subject = 'ela'
        grade = 10
        assessment_list = generate_dim_assessment()
        actual_filtered_assessments = gen_assessment_outcome.get_filtered_assessments(subject, grade, assessment_list)
        self.assertEqual(len(actual_filtered_assessments), len(ASSMT_SCORE_YEARS) * 4)
        for assessment in actual_filtered_assessments:
            self.assertEqual(assessment.asmt_grade, grade)
            self.assertEqual(assessment.asmt_subject.lower(), subject.lower())

    def test_create_date_taken_BOY(self):
        year = 2012
        period = 'BOY'
        actual_date = gen_assessment_outcome.create_date_taken(year, period)
        self.assertEqual(actual_date.year, year)
        self.assertTrue(actual_date.month in [9, 10])
        self.assertTrue(actual_date.month in range(1, 29))

    def test_create_date_taken_MOY(self):
        year = 2012
        period = 'MOY'
        actual_date = gen_assessment_outcome.create_date_taken(year, period)
        self.assertTrue(actual_date.month in [11, 12, 1, 2, 3])
        if actual_date.month in [11, 12]:
            self.assertEqual(actual_date.year, year)
        else:
            self.assertEqual(actual_date.year, year + 1)
        self.assertTrue(actual_date.month in range(1, 29))

    def test_create_date_taken_EOY(self):
        year = 2012
        period = 'EOY'
        actual_date = gen_assessment_outcome.create_date_taken(year, period)
        self.assertEqual(actual_date.year, year + 1)
        self.assertTrue(actual_date.month in [4, 5, 6])
        self.assertTrue(actual_date.month in range(1, 29))

    def test_generate_single_assessment_outcome_from_student_info(self):
        assessment = make_an_assessment('ELA')
        students = make_students_list(1)
        student = students[0]
        inst_hier_rec_id = 81723
        where_taken = WhereTaken(91845, 'where_taken_test_name')
        subject_name = 'Math'
        row = {'student_id': student.student_id,
               'teacher_id': student.teacher_id,
               'state_code': student.state_code,
               'district_id': student.district_id,
               'school_id': student.school_id,
               'section_id': student.section_id,
               'inst_hier_rec_id': inst_hier_rec_id,
               'section_rec_id': student.section_rec_id,
               'where_taken_id': where_taken.where_taken_id,
               'where_taken_name': where_taken.where_taken_name,
               'enrl_grade': student.grade,
               'subject_name': subject_name,
               }
        actual_assessment_outcome = gen_assessment_outcome.generate_single_assessment_outcome_from_student_info(assessment, row)
        self.assertIsInstance(actual_assessment_outcome, AssessmentOutcome)

    def test_generate_assessment_score_four_claims(self):
        assessment = make_an_assessment('ELA')
        assessment_score = gen_assessment_outcome.generate_assessment_score(assessment)
        self.assertIsInstance(assessment_score, AssessmentScore)
        self.assertTrue(MINIMUM_ASSESSMENT_SCORE <= assessment_score.overall_score <= MAXIMUM_ASSESSMENT_SCORE)
        self.assertTrue(1 <= assessment_score.perf_lvl <= 4)
        self.assertTrue(assessment_score.interval_min > assessment.asmt_score_min)
        self.assertTrue(assessment_score.interval_max < assessment.asmt_score_max)
        self.assertEqual(len(assessment_score.claim_scores), 4)

    def test_generate_assessment_score_three_claims(self):
        assessment = make_an_assessment('Math')
        assessment_score = gen_assessment_outcome.generate_assessment_score(assessment)
        self.assertIsInstance(assessment_score, AssessmentScore)
        self.assertTrue(MINIMUM_ASSESSMENT_SCORE <= assessment_score.overall_score <= MAXIMUM_ASSESSMENT_SCORE)
        self.assertTrue(1 <= assessment_score.perf_lvl <= 4)
        self.assertTrue(assessment_score.interval_min > assessment.asmt_score_min)
        self.assertTrue(assessment_score.interval_max < assessment.asmt_score_max)
        self.assertEqual(len(assessment_score.claim_scores), 3)

    def test_calculate_performance_level_boundry_value(self):
        score = 2100
        asmt_cut_point_3 = 2100
        asmt_cut_point_2 = 1800
        asmt_cut_point_1 = 120
        expected_performance_level = 4
        actual_performance_level = gen_assessment_outcome.calculate_performance_level(score, asmt_cut_point_3, asmt_cut_point_2, asmt_cut_point_1)
        self.assertEqual(expected_performance_level, actual_performance_level)

    def test_calculate_performance_level_between_two_levels(self):
        score = 1723
        asmt_cut_point_3 = 2100
        asmt_cut_point_2 = 1800
        asmt_cut_point_1 = 120
        expected_performance_level = 2
        actual_performance_level = gen_assessment_outcome.calculate_performance_level(score, asmt_cut_point_3, asmt_cut_point_2, asmt_cut_point_1)
        self.assertEqual(expected_performance_level, actual_performance_level)

    def test_generate_plus_minus_normal_overall_score(self):
        overall_score = 1912
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_plus_minus = 36
        actual_plus_minus = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(expected_plus_minus, actual_plus_minus)

    def test_generate_plus_minus_small_overall_score(self):
        overall_score = 1201
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_plus_minus = 0
        actual_plus_minus = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(expected_plus_minus, actual_plus_minus)

    def test_generate_plus_minus_high_overall_score(self):
        overall_score = 2390
        average_score = 1800.0
        standard_deviation = 150.0
        minimum = 1200
        maximum = 2400
        expected_plus_minus = 0
        actual_plus_minus = gen_assessment_outcome.generate_plus_minus(overall_score, average_score, standard_deviation, minimum, maximum)
        self.assertEqual(expected_plus_minus, actual_plus_minus)

    def test_generate_claim_scores_for_math(self):
        assessment_score = 1670
        assessment = make_an_assessment('Math')
        actual_claim_scores = gen_assessment_outcome.generate_claim_scores(assessment_score, assessment)
        self.assertEqual(len(actual_claim_scores), 3)

    def test_generate_claim_scores_for_ela(self):
        assessment_score = 2370
        assessment = make_an_assessment('ELA')
        actual_claim_scores = gen_assessment_outcome.generate_claim_scores(assessment_score, assessment)
        self.assertEqual(len(actual_claim_scores), 4)

    def test_rescale_value(self):
        old_value = 245
        old_scale = [50, 500]
        new_scale = [1200, 2400]
        expected_rescaled_value = (old_value - old_scale[0]) * (new_scale[1] - new_scale[0]) / (old_scale[1] - old_scale[0]) + new_scale[0]
        actual_rescaled_value = gen_assessment_outcome.rescale_value(old_value, old_scale, new_scale)
        self.assertEqual(expected_rescaled_value, actual_rescaled_value)

    def test_calculate_claim_average_score(self):
        minimum = 35
        maximum = 90
        expected_claim_average_score = (minimum + maximum) / 2
        actual_claim_average_score = gen_assessment_outcome.calculate_claim_average_score(minimum, maximum)
        self.assertEqual(expected_claim_average_score, actual_claim_average_score)

    def test_calculate_claim_standard_deviation(self):
        average = 45
        minimum = 20
        expected_claim_standard_deviation = (average - minimum) / 4
        actual_claim_standard_deviation = gen_assessment_outcome.calculate_claim_standard_deviation(average, minimum)
        self.assertEqual(expected_claim_standard_deviation, actual_claim_standard_deviation)


def make_an_assessment(subject):
    number_of_claims = 4 if subject.lower == 'ELA'.lower else 3
    params = {'asmt_rec_id': 1234,
              'asmt_id': 273491,
              'asmt_type': 'SUMMATIVE',
              'asmt_period': 'EOY',
              'asmt_period_year': 2012,
              'asmt_version': 'V1',
              'asmt_grade': 1,
              'asmt_subject': subject,
              'from_date': '20120101',
              'claim_list': make_claim_list(number_of_claims),
              'asmt_score_min': 1200,
              'asmt_score_max': 2400,
              'asmt_cut_point_1': 1400,
              'asmt_cut_point_2': 1800,
              'asmt_cut_point_3': 2100,
              }
    assessment = Assessment(**params)
    return assessment


def make_claim_list(number_of_claims):
    claims = []
    if number_of_claims == 4:
        weights = [0.25, 0.15, 0.35, 0.25]
    elif number_of_claims == 3:
        weights = [0.25, 0.45, 0.2]
    else:
        return None
    for i in range(number_of_claims):
        claim_name = 'claim ' + str(i + 1)
        claim_score_min = 14
        claim_score_max = 95
        claim_score_weight = weights[i]
        claim = Claim(claim_name, claim_score_min, claim_score_max, claim_score_weight)
        claims.append(claim)
    return claims


def make_students_list(number_of_students):
    # make student_bio_info objects
    student_bio_info = []
    for index in range(number_of_students):
        student_rec_id = index
        student_id = 1000 - student_rec_id
        first_name = 'first_name' + str(index)
        last_name = 'last_name' + str(index)
        address_1 = 'address' + str(index)
        dob = '1998'
        district_id = 98124
        state_code = 'DE'
        gender = 'male'
        email = 'email' + str(index)
        school_id = 91827
        zip_code = 99876
        city = 'city name'
        student_bio_info.append(StudentBioInfo(student_rec_id, student_id, first_name, last_name, address_1, dob, district_id, state_code, gender, email, school_id, zip_code, city))

    # make student objects
    students = []
    for student_bio in student_bio_info:
        student_params = {
            'student_bio_info': student_bio,
            'section_id': index + 3000,
            'grade': 5,
            'from_date': '20120901',
            'to_date': '29990901',
            'most_recent': True,
            'teacher_id': index + 7000,
            'section_rec_id': index + 9000
        }
        student = Student(**student_params)
        students.append(student)
    return students
