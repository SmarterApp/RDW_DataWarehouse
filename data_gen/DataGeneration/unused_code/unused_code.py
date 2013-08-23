'''
Created on Aug 23, 2013

@author: swimberly
'''


def generate_fact_assessment_outcome(asmt_rec_id, student_guid, teacher_guid, state_code, district_guid, school_guid, section_guid,
                                     inst_hier_rec_id, section_rec_id, where_taken_id, where_taken_name, asmt_grade, enrl_grade,
                                     date_taken, date_taken_day, date_taken_month, date_taken_year, asmt_score, asmt_score_range_min,
                                     asmt_score_range_max, asmt_perf_lvl,
                                     asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                                     asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                                     asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                                     asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max,
                                     batch_guid):
    id_generator = IdGen()
    asmnt_outcome_rec_id = id_generator.get_id()

    status = 'C'
    most_recent = True

    asmt_outcome = AssessmentOutcome(asmnt_outcome_rec_id, asmt_rec_id, student_guid,
                                     teacher_guid, state_code, district_guid, school_guid, section_guid, inst_hier_rec_id, section_rec_id,
                                     where_taken_id, where_taken_name, asmt_grade, enrl_grade, date_taken, date_taken_day,
                                     date_taken_month, date_taken_year, asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                                     asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                                     asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                                     asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                                     asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max,
                                     status, most_recent, batch_guid)

    return asmt_outcome


# TODO: Move this function somewhere else (generate_data?) since it uses helper_entities (students, scores)
def generate_fact_assessment_outcomes(students, scores, asmt_rec_id, teacher_guid, state_code, district_guid, school_guid, section_guid,
                                      inst_hier_rec_id, section_rec_id, where_taken_id, where_taken_name, asmt_grade, enrl_grade,
                                      date_taken, date_taken_day, date_taken_month, date_taken_year, batch_guid):
    '''
    Generates AssessmentOutcome objects for each student in 'students' using the scores in 'scores'
    Scores are assigned in the order of the score list
    @return: A list of AssessmentOutcome objects
    '''

    outcomes = []

    for student in students:
        score = scores.pop(0)
        # TODO: Create a function that unpacks score information, or break this function down into some other functions.
        claim_scores = score.claim_scores

        student_guid = student.student_guid
        asmt_score = score.overall_score
        asmt_score_range_min = score.interval_min
        asmt_score_range_max = score.interval_max
        asmt_perf_lvl = score.perf_lvl
        asmt_claim_1_score = claim_scores[0].claim_score
        asmt_claim_2_score = claim_scores[1].claim_score
        asmt_claim_3_score = claim_scores[2].claim_score
        asmt_claim_4_score = claim_scores[3].claim_score if len(claim_scores) > 3 else None
        asmt_claim_1_score_range_min = claim_scores[0].claim_score_interval_minimum
        asmt_claim_2_score_range_min = claim_scores[1].claim_score_interval_minimum
        asmt_claim_3_score_range_min = claim_scores[2].claim_score_interval_minimum
        asmt_claim_4_score_range_min = claim_scores[3].claim_score_interval_minimum if len(claim_scores) > 3 else None
        asmt_claim_1_score_range_max = claim_scores[0].claim_score_interval_maximum
        asmt_claim_2_score_range_max = claim_scores[1].claim_score_interval_maximum
        asmt_claim_3_score_range_max = claim_scores[2].claim_score_interval_maximum
        asmt_claim_4_score_range_max = claim_scores[3].claim_score_interval_maximum if len(claim_scores) > 3 else None

        asmt_outcome = generate_fact_assessment_outcome(asmt_rec_id, student_guid, teacher_guid, state_code, district_guid, school_guid, section_guid,
                                                        inst_hier_rec_id, section_rec_id, where_taken_id, where_taken_name, asmt_grade, enrl_grade,
                                                        date_taken, date_taken_day, date_taken_month, date_taken_year, asmt_score, asmt_score_range_min, asmt_score_range_max, asmt_perf_lvl,
                                                        asmt_claim_1_score, asmt_claim_1_score_range_min, asmt_claim_1_score_range_max,
                                                        asmt_claim_2_score, asmt_claim_2_score_range_min, asmt_claim_2_score_range_max,
                                                        asmt_claim_3_score, asmt_claim_3_score_range_min, asmt_claim_3_score_range_max,
                                                        asmt_claim_4_score, asmt_claim_4_score_range_min, asmt_claim_4_score_range_max,
                                                        batch_guid)
        outcomes.append(asmt_outcome)

    return outcomes
