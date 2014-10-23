'''
Created on Oct 21, 2014

@author: tosako
'''
from string import capwords
from smarter.reports.helpers.filters import get_student_demographic
from smarter.reports.helpers.constants import Constants
from smarter.reports.helpers.assessments import get_claims, \
    get_overall_asmt_interval


def get_group_filters(results):
    # TODO: use list comprehension, format grouping information for filters
    all_groups = set()
    for result in results:
        for i in range(1, 11):
            if result['group_{i}_id'.format(i=i)]:
                all_groups.add((result['group_{i}_id'.format(i=i)], result['group_{i}_text'.format(i=i)]))

    options = [{"value": k, "label": v} for k, v in all_groups]
    filters = sorted(options, key=lambda k: k['label'])
    return filters


def __reverse_map(map_object):
    '''
    reverse map for FE
    '''
    return {v: k for k, v in map_object.items()}


def format_assessments(results, subjects_map, iab=False):
    '''
    Format student assessments.
    '''

    assessments = {}
    # Formatting data for Front End
    for result in results:
        effectiveDate = result['effective_date']  # e.g. 20140401
        asmtDict = assessments.get(effectiveDate, {})
        asmtType = capwords(result['asmt_type'], ' ')  # Summative, Interim
        asmtList = asmtDict.get(asmtType, {})
        studentId = result['student_id']  # e.g. student_1

        student = asmtList.get(studentId, {})
        student['student_id'] = studentId
        student['student_first_name'] = result['first_name']
        student['student_middle_name'] = result['middle_name']
        student['student_last_name'] = result['last_name']
        student['enrollment_grade'] = result['enrollment_grade']
        student['state_code'] = result['state_code']
        student['demographic'] = get_student_demographic(result)
        student[Constants.ROWID] = result['student_id']

        subject = subjects_map[result['asmt_subject']]
        assessment = student.get(subject, {})
        assessment['group'] = []  # for student group filter
        for i in range(1, 11):
            if result['group_{count}_id'.format(count=i)] is not None:
                assessment['group'].append(result['group_{count}_id'.format(count=i)])
        assessment['asmt_grade'] = result['asmt_grade']
        assessment['asmt_perf_lvl'] = result['asmt_perf_lvl']
        if iab:
            number_of_claims = 1
            include_names = True
        else:
            number_of_claims = 4
            include_names = False
            assessment['asmt_score'] = result['asmt_score']
            assessment['asmt_score_range_min'] = result['asmt_score_range_min']
            assessment['asmt_score_range_max'] = result['asmt_score_range_max']
            assessment['asmt_score_interval'] = get_overall_asmt_interval(result)
        assessment['claims'] = get_claims(number_of_claims=number_of_claims, result=result, include_scores=True, include_names=include_names)

        student[subject] = assessment
        asmtList[studentId] = student
        asmtDict[asmtType] = asmtList
        assessments[effectiveDate] = asmtDict
    return assessments
