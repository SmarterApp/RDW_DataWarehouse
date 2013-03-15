from datetime import date
from idgen import IdGen
import random
import uuid
from entities import AssessmentOutcome
from helper_entities import AssessmentScore, ClaimScore
from constants import SUBJECTS
import py1


def generate_assessment_outcomes_from_student_list(assessment_list, students, grade, subject, inst_hier_rec_id, where_taken):
    assessment_outcomes = []
    filtered_assessments = get_filtered_assessments(subject, grade, assessment_list)
    for student in students:
        for assessment in filtered_assessments:
            date_taken = create_date_taken(assessment.asmt_period_year, assessment.asmt_period)
            assessment_outcome = generate_single_assessment_outcome_from_student(assessment, student, inst_hier_rec_id, where_taken, date_taken)
            assessment_outcomes.append(assessment_outcome)
    return assessment_outcomes

def generate_single_assessment_outcome_from_student(assessment, student, inst_hier_rec_id, where_taken, date_taken):

    asmt_score = generate_assessment_score(assessment)
    id_generator = IdGen()

    # Some assessment_scores will have 4 claims, some will have 3
    # If only 3 claims, make claim_4 fields 'None'
    if len(asmt_score.claim_scores) == 4:
        asmt_claim_4_score =  asmt_score.claim_scores[3].claim_score
        asmt_claim_4_score_range_min = asmt_score.claim_scores[3].claim_score_interval_minimum
        asmt_claim_4_score_range_max= asmt_score.claim_scores[3].claim_score_interval_maximum
    else:
        asmt_claim_4_score =  None
        asmt_claim_4_score_range_min = None
        asmt_claim_4_score_range_max= None


    params = {
        'asmnt_outcome_id': uuid.uuid4(),
        'asmnt_outcome_external_id': id_generator.get_id(),
        'asmt_rec_id': assessment.asmt_rec_id,
        'student_id': student.student_id,
        'teacher_id': student.teacher_id,
        'state_code': student.state_code,
        'district_id': student.district_id,
        'school_id': student.school_id,
        'section_id': student.section_id,
        'inst_hier_rec_id': inst_hier_rec_id,
        'section_rec_id': student.section_rec_id,
        'where_taken_id': where_taken.where_taken_id,
        'where_taken_name': where_taken.where_taken_name,
        'asmt_grade': student.grade,
        'enrl_grade': student.grade,
        'date_taken': date_taken.strftime('%Y%m%d'),
        'date_taken_day': date_taken.day,
        'date_taken_month': date_taken.month,
        'date_taken_year': date_taken.year,

        # Overall Assessment Data
        'asmt_score': asmt_score.overall_score,
        'asmt_score_range_min': asmt_score.interval_min,
        'asmt_score_range_max':asmt_score.interval_max,
        'asmt_perf_lvl': asmt_score.perf_lvl,

        # Assessment Claim Data
        'asmt_claim_1_score': asmt_score.claim_scores[0].claim_score,
        'asmt_claim_1_score_range_min': asmt_score.claim_scores[0].claim_score_interval_minimum,
        'asmt_claim_1_score_range_max': asmt_score.claim_scores[0].claim_score_interval_maximum,

        'asmt_claim_2_score': asmt_score.claim_scores[1].claim_score,
        'asmt_claim_2_score_range_min': asmt_score.claim_scores[1].claim_score_interval_minimum,
        'asmt_claim_2_score_range_max': asmt_score.claim_scores[1].claim_score_interval_maximum,

        'asmt_claim_3_score': asmt_score.claim_scores[2].claim_score,
        'asmt_claim_3_score_range_min': asmt_score.claim_scores[2].claim_score_interval_minimum,
        'asmt_claim_3_score_range_max': asmt_score.claim_scores[2].claim_score_interval_maximum,

        # These fields may or may not be null (Some have a 4th claim, others don't)
        'asmt_claim_4_score': asmt_claim_4_score,
        'asmt_claim_4_score_range_min': asmt_claim_4_score_range_min,
        'asmt_claim_4_score_range_max': asmt_claim_4_score_range_max,

        'asmt_create_date': asmt_score.asmt_create_date,
        'status': 'IR',
        'most_recent': True
    }

    assessment_outcome = AssessmentOutcome(**params)
    return assessment_outcome

def generate_assessment_outcomes_from_query(assessment_list, rows):
    assessment_outcomes = []
    for row in rows:
        filtered_assessments = get_filtered_assessments(row['subject_name'], row['enrl_grade'], assessment_list)
        for assessment in filtered_assessments:
            assessment_outcome = generate_single_assessment_outcome_from_row(assessment, row)
            assessment_outcomes.append(assessment_outcome)
    return assessment_outcomes

def generate_single_assessment_outcome_from_row(assessment, row):
    id_generator = IdGen()
    todays_date = date.today()
    asmt_score = generate_assessment_score(assessment)

    if len(asmt_score.claim_scores) == 4:
        asmt_claim_4_score = asmt_score.claim_scores[3].claim_score
        asmt_claim_4_score_range_min = asmt_score.claim_scores[3].claim_score_interval_minimum
        asmt_claim_4_score_range_max = asmt_score.claim_scores[3].claim_score_interval_maximum
    else:
        asmt_claim_4_score = None
        asmt_claim_4_score_range_min = None
        asmt_claim_4_score_range_max = None

    params = {
        'asmnt_outcome_id': uuid.uuid4(),
        'asmnt_outcome_external_id': id_generator.get_id(),
        'asmt_rec_id': assessment.asmt_rec_id,
        'student_id': row['student_id'],
        'teacher_id': row['teacher_id'],
        'state_code': row['state_code'],
        'district_id': row['district_id'],
        'school_id': row['school_id'],
        'section_id': row['section_id'],
        'inst_hier_rec_id': row['inst_hier_rec_id'],
        'section_rec_id': row['section_rec_id'],
        'where_taken_id': uuid.uuid4(),
        'where_taken_name': row['school_name'],
        'asmt_grade': row['enrl_grade'],
        'enrl_grade': row['enrl_grade'],
        'date_taken': todays_date.strftime('%Y%m%d'),
        'date_taken_day': todays_date.day,
        'date_taken_month': todays_date.month,
        'date_taken_year': todays_date.year,

        # Overall Assessment Data
        'asmt_score': asmt_score.overall_score,
        'asmt_score_range_min': asmt_score.interval_min,
        'asmt_score_range_max':asmt_score.interval_max,
        'asmt_perf_lvl': asmt_score.perf_lvl,

        # Assessment Claim Data
        'asmt_claim_1_score': asmt_score.claim_scores[0].claim_score,
        'asmt_claim_1_score_range_min': asmt_score.claim_scores[0].claim_score_interval_minimum,
        'asmt_claim_1_score_range_max': asmt_score.claim_scores[0].claim_score_interval_maximum,

        'asmt_claim_2_score': asmt_score.claim_scores[1].claim_score,
        'asmt_claim_2_score_range_min': asmt_score.claim_scores[1].claim_score_interval_minimum,
        'asmt_claim_2_score_range_max': asmt_score.claim_scores[1].claim_score_interval_maximum,

        'asmt_claim_3_score': asmt_score.claim_scores[2].claim_score,
        'asmt_claim_3_score_range_min': asmt_score.claim_scores[2].claim_score_interval_minimum,
        'asmt_claim_3_score_range_max': asmt_score.claim_scores[2].claim_score_interval_maximum,

        # These fields may or may not be null (Some have a 4th claim, others don't)
        'asmt_claim_4_score': asmt_claim_4_score,
        'asmt_claim_4_score_range_min': asmt_claim_4_score_range_min,
        'asmt_claim_4_score_range_max': asmt_claim_4_score_range_max,

        'asmt_create_date': asmt_score.asmt_create_date,
        'status': 'IR',
        'most_recent': True
    }
    assessment_outcome = AssessmentOutcome(**params)

    return assessment_outcome


def get_filtered_assessments(subject, grade, assessment_list):
    filtered_assessments = []
    for assessment in assessment_list:
        if assessment.asmt_subject.lower() == subject.lower() and int(assessment.asmt_grade) == int(grade):
                filtered_assessments.append(assessment)
    return filtered_assessments


def create_date_taken(year, period):
    dates_taken_map = generate_dates_taken(int(year))
    date_taken = dates_taken_map[period]
    return date_taken


def generate_dates_taken(year):
    '''
    generates a list of dates for a given year when tests are taken
    three dates correspond to BOY, MOY, EOY
    returns a dict containing three dates with keys: 'BOY', 'MOY', 'EOY'
    '''
    boy_pool = [9, 10]
    moy_pool = [11, 12, 1, 2, 3]
    eoy_pool = [4, 5, 6]

    boy_date = date(year, random.choice(boy_pool), random.randint(1, 28))

    moy_month = random.choice(moy_pool)
    moy_year = year
    if moy_month <= 3:
        moy_year += 1
    moy_date = date(moy_year, moy_month, random.randint(1, 28))
    eoy_date = date(year + 1, random.choice(eoy_pool), random.randint(1, 28))

    return {'BOY': boy_date, 'MOY': moy_date, 'EOY': eoy_date}


def generate_assessment_score(assessment):
    average = assessment.average_score
    standard_deviation = assessment.standard_deviation
    minimum = assessment.score_minimum
    maximum = assessment.score_maximum

    overall_score = int(py1.extract_value_from_normal_distribution(average, standard_deviation, minimum, maximum))
    performance_level = calculate_performance_level(overall_score, assessment.asmt_cut_point_3, assessment.asmt_cut_point_2, assessment.asmt_cut_point_1)

    plus_minus = generate_plus_minus(overall_score, average, standard_deviation, minimum, maximum)
    interval_minimum = int(overall_score - plus_minus)
    interval_maximum = int(overall_score + plus_minus)

    claim_scores = generate_claim_scores(overall_score, assessment)

    params = {
        'overall_score': overall_score,
        'perf_lvl': performance_level,
        'interval_min': interval_minimum,
        'interval_max': interval_maximum,
        'claim_scores': claim_scores,
        'asmt_create_date': date(2012, 3, 13).strftime('%Y%m%d')
    }

    assessment_score = AssessmentScore(**params)
    return assessment_score


def calculate_performance_level(score, asmt_cut_point_3, asmt_cut_point_2, asmt_cut_point_1):
    '''
    calculates a performance level as an integer based on a students overall score and
    the cutoffs for the assessment (0, 1 or 2)
    score -- a score object
    assessment -- an assessment object
    '''
    # print(asmt.asmt_cut_point_3, asmt.asmt_cut_point_2, asmt.asmt_cut_point_1, score)
    if score >= asmt_cut_point_3:
        return 4
    elif score >= asmt_cut_point_2:
        return 3
    elif score >= asmt_cut_point_1:
        return 2
    else:
        return 1


def generate_plus_minus(score, average_score, standard_deviation, minimum, maximum):
    # calculate the difference between the score and the average score
    difference = abs(average_score - score)
    # divide this difference by the standard deviation, and you'll have
    # the number of standard deviations between the score and the average

    number_of_standard_deviations = difference / standard_deviation

    # we use the number of standard deviations to determine the value added to and subtracted from
    # the score (the endpoints of the confidence interval)
    # this number should be large when the score is near average
    # and small when closer to the min/max
    if number_of_standard_deviations <= 1:
        # 2% of the average score
        plus_minus = .02 * average_score
    elif number_of_standard_deviations <= 2:
        # 1% of the average score
        plus_minus = .01 * average_score
    elif number_of_standard_deviations <= 3:
        # .5% of the average score
        plus_minus = .005 * average_score
    else:
        # 0
        plus_minus = 0
    # ensure that the endpoints of our confidence interval falls within the min/max of our score range
    if (score + plus_minus <= maximum) and (score - plus_minus >= minimum):
        return plus_minus
    else:
        raise Exception('Acceptable range:%d - %d, interval boundaries are %d - %d' % (minimum, maximum, score + plus_minus, score - plus_minus))


def generate_claim_scores(assessment_score, assessment):
    claim_scores = []
    for claim in assessment.get_claim_list():

        # Get basic claim information from claim object
        claim_minimum_score = claim.claim_score_min
        claim_maximum_score = claim.claim_score_max
        claim_score_scale = (claim_minimum_score, claim_maximum_score)
        claim_weight = claim.claim_score_weight

        # calculate the claim score
        weighted_assessment_scale = (assessment.score_minimum * claim_weight, assessment.score_maximum * claim_weight)
        unscaled_claim_score = assessment_score * claim_weight
        scaled_claim_score = int(rescale_value(unscaled_claim_score, weighted_assessment_scale, claim_score_scale))
        claim_average_score = calculate_claim_average_score(claim_minimum_score, claim_maximum_score)
        claim_standard_deviation = calculate_claim_standard_deviation(claim_average_score, claim_minimum_score)
        claim_plus_minus = generate_plus_minus(scaled_claim_score, claim_average_score, claim_standard_deviation, claim_minimum_score, claim_maximum_score)
        claim_interval_min = int(scaled_claim_score - claim_plus_minus)
        claim_interval_max = int(scaled_claim_score + claim_plus_minus)

        claim_score = ClaimScore(scaled_claim_score, claim_interval_min, claim_interval_max)

        claim_scores.append(claim_score)
    return claim_scores


# see http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
# for a complete explanation of this logic
def rescale_value(old_value, old_scale, new_scale):
    '''
        old_scale and new_scale are tuples
        the first value represents the minimum score
        the second value represents the maximu score
    '''

    old_min = old_scale[0]
    old_max = old_scale[1]

    new_min = new_scale[0]
    new_max = new_scale[1]

    numerator = (new_max - new_min) * (old_value - old_min)
    denominator = old_max - old_min

    result = (numerator / denominator) + new_min
    return result


def calculate_claim_average_score(minimum, maximum):
    # TODO: Is it easier to calculate as: (minimum +  maximum) / 2
    # assuming the average is in the middle of the range of scores
    difference = maximum - minimum
    half_difference = difference / 2
    average = minimum + half_difference
    return average


def calculate_claim_standard_deviation(average, minimum):
    # find the difference between the average and the minimum
    difference = average - minimum
    # Approximately 4 standard deviations should exist between the average and the min
    standard_deviation = difference / 4
    return standard_deviation
