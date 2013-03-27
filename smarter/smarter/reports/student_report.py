'''
Created on Jan 13, 2013

@author: tosako
'''


from edapi.decorators import report_config, user_info
from smarter.reports.helpers.name_formatter import format_full_name
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_
from edapi.exceptions import NotFoundException
from string import capwords
from smarter.database.connector import SmarterDBConnection
from edapi.logging import audit_event
from smarter.reports.helpers.breadcrumbs import get_breadcrumbs_context
from smarter.reports.helpers.assessments import get_cut_points,\
    get_overall_asmt_interval, get_claims


def __prepare_query(connector, student_guid, assessment_guid):
    # get table metadatas
    fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
    dim_student = connector.get_table('dim_student')
    dim_asmt = connector.get_table('dim_asmt')
    dim_staff = connector.get_table('dim_staff')
    query = select([fact_asmt_outcome.c.student_guid,
                    dim_student.c.first_name.label('student_first_name'),
                    dim_student.c.middle_name.label('student_middle_name'),
                    dim_student.c.last_name.label('student_last_name'),
                    dim_student.c.grade.label('grade'),
                    dim_student.c.district_guid.label('district_guid'),
                    dim_student.c.school_guid.label('school_guid'),
                    dim_student.c.state_code.label('state_code'),
                    dim_asmt.c.asmt_subject.label('asmt_subject'),
                    dim_asmt.c.asmt_period.label('asmt_period'),
                    dim_asmt.c.asmt_type.label('asmt_type'),
                    dim_asmt.c.asmt_score_min.label('asmt_score_min'),
                    dim_asmt.c.asmt_score_max.label('asmt_score_max'),
                    dim_asmt.c.asmt_perf_lvl_name_1.label("asmt_cut_point_name_1"),
                    dim_asmt.c.asmt_perf_lvl_name_2.label("asmt_cut_point_name_2"),
                    dim_asmt.c.asmt_perf_lvl_name_3.label("asmt_cut_point_name_3"),
                    dim_asmt.c.asmt_perf_lvl_name_4.label("asmt_cut_point_name_4"),
                    dim_asmt.c.asmt_perf_lvl_name_5.label("asmt_cut_point_name_5"),
                    dim_asmt.c.asmt_cut_point_1.label("asmt_cut_point_1"),
                    dim_asmt.c.asmt_cut_point_2.label("asmt_cut_point_2"),
                    dim_asmt.c.asmt_cut_point_3.label("asmt_cut_point_3"),
                    dim_asmt.c.asmt_cut_point_4.label("asmt_cut_point_4"),
                    dim_asmt.c.asmt_custom_metadata.label('asmt_custom_metadata'),
                    fact_asmt_outcome.c.asmt_grade.label('asmt_grade'),
                    fact_asmt_outcome.c.asmt_score.label('asmt_score'),
                    fact_asmt_outcome.c.asmt_score_range_min.label('asmt_score_range_min'),
                    fact_asmt_outcome.c.asmt_score_range_max.label('asmt_score_range_max'),
                    fact_asmt_outcome.c.date_taken_day.label('date_taken_day'),
                    fact_asmt_outcome.c.date_taken_month.label('date_taken_month'),
                    fact_asmt_outcome.c.date_taken_year.label('date_taken_year'),
                    fact_asmt_outcome.c.asmt_perf_lvl.label('asmt_perf_lvl'),
                    dim_asmt.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                    dim_asmt.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                    dim_asmt.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                    dim_asmt.c.asmt_claim_4_name.label('asmt_claim_4_name'),
                    dim_asmt.c.asmt_claim_1_score_min.label('asmt_claim_1_score_min'),
                    dim_asmt.c.asmt_claim_2_score_min.label('asmt_claim_2_score_min'),
                    dim_asmt.c.asmt_claim_3_score_min.label('asmt_claim_3_score_min'),
                    dim_asmt.c.asmt_claim_4_score_min.label('asmt_claim_4_score_min'),
                    dim_asmt.c.asmt_claim_1_score_max.label('asmt_claim_1_score_max'),
                    dim_asmt.c.asmt_claim_2_score_max.label('asmt_claim_2_score_max'),
                    dim_asmt.c.asmt_claim_3_score_max.label('asmt_claim_3_score_max'),
                    dim_asmt.c.asmt_claim_4_score_max.label('asmt_claim_4_score_max'),
                    fact_asmt_outcome.c.asmt_claim_1_score.label('asmt_claim_1_score'),
                    fact_asmt_outcome.c.asmt_claim_2_score.label('asmt_claim_2_score'),
                    fact_asmt_outcome.c.asmt_claim_3_score.label('asmt_claim_3_score'),
                    fact_asmt_outcome.c.asmt_claim_4_score.label('asmt_claim_4_score'),
                    fact_asmt_outcome.c.asmt_claim_1_score_range_min.label('asmt_claim_1_score_range_min'),
                    fact_asmt_outcome.c.asmt_claim_2_score_range_min.label('asmt_claim_2_score_range_min'),
                    fact_asmt_outcome.c.asmt_claim_3_score_range_min.label('asmt_claim_3_score_range_min'),
                    fact_asmt_outcome.c.asmt_claim_4_score_range_min.label('asmt_claim_4_score_range_min'),
                    fact_asmt_outcome.c.asmt_claim_1_score_range_max.label('asmt_claim_1_score_range_max'),
                    fact_asmt_outcome.c.asmt_claim_2_score_range_max.label('asmt_claim_2_score_range_max'),
                    fact_asmt_outcome.c.asmt_claim_3_score_range_max.label('asmt_claim_3_score_range_max'),
                    fact_asmt_outcome.c.asmt_claim_4_score_range_max.label('asmt_claim_4_score_range_max'),
                    dim_staff.c.first_name.label('teacher_first_name'),
                    dim_staff.c.middle_name.label('teacher_middle_name'),
                    dim_staff.c.last_name.label('teacher_last_name')],
                   from_obj=[fact_asmt_outcome
                             .join(dim_student, and_(fact_asmt_outcome.c.student_guid == dim_student.c.student_guid,
                                                     fact_asmt_outcome.c.section_guid == dim_student.c.section_guid))
                             .join(dim_staff, and_(fact_asmt_outcome.c.teacher_guid == dim_staff.c.staff_guid,
                                                   fact_asmt_outcome.c.section_guid == dim_staff.c.section_guid,
                                                   dim_staff.c.most_recent))
                             .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id,
                                                  dim_asmt.c.most_recent,
                                                  dim_asmt.c.asmt_type == 'SUMMATIVE'))])
    query = query.where(and_(fact_asmt_outcome.c.most_recent, fact_asmt_outcome.c.status == 'C', fact_asmt_outcome.c.student_guid == student_guid))
    if assessment_guid is not None:
        query = query.where(dim_asmt.c.asmt_guid == assessment_guid)
    query = query.order_by(dim_asmt.c.asmt_subject.desc())
    return query


def __arrange_results(results):
    '''
    This method arranges the data retreievd from the db to make it easier to consume by the client
    '''
    for result in results:

        result['teacher_full_name'] = format_full_name(result['teacher_first_name'], result['teacher_middle_name'], result['teacher_last_name'])

        # asmt_type is an enum, so we would to capitalize it to make it presentable
        result['asmt_type'] = capwords(result['asmt_type'], ' ')

        result['asmt_score_interval'] = get_overall_asmt_interval(result)

        # format and rearrange cutpoints
        result = get_cut_points(result)

        result['claims'] = get_claims(number_of_claims=5, result=result)

    # rearranging the json so we could use it more easily with mustache
    results = {"items": results}
    return results


@report_config(name='individual_student_report',
               params={
                    "studentGuid": {
                        "type": "string",
                        "required": True,
                        "pattern": "^[a-zA-Z0-9\-]{0,50}$"},
                    "assessmentGuid": {
                        "name": "student_assessments_report",
                        "type": "string",
                        "required": False,
                        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
                    },
               })
@audit_event()
@user_info
def get_student_report(params):
    '''
    report for student and student_assessment
    '''
    # get studentId
    student_guid = str(params['studentGuid'])

    # if assessmentId is available, read the value.
    assessment_guid = None
    if 'assessmentGuid' in params:
        assessment_guid = str(params['assessmentGuid'])

    with SmarterDBConnection() as connection:
        query = __prepare_query(connection, student_guid, assessment_guid)

        result = connection.get_result(query)
        if result:
            first_student = result[0]
            student_name = format_full_name(first_student['student_first_name'], first_student['student_middle_name'], first_student['student_last_name'])
            context = get_breadcrumbs_context(district_guid=first_student['district_guid'], school_guid=first_student['school_guid'], asmt_grade=first_student['grade'], student_name=student_name)
        else:
            raise NotFoundException("There are no results for student id {0}".format(student_guid))

        # prepare the result for the client
        result = __arrange_results(result)

        result['context'] = context

        return result


@report_config(name='student_assessments_report',
               params={
                   "studentGuid": {
                   "type": "string",
                   "required": True
                   }
               }
               )
def get_student_assessment(params):

    # get studentId
    student_guid = params['studentGuid']

    with SmarterDBConnection() as connection:
        # get table metadatas
        dim_asmt = connection.get_table('dim_asmt')
        fact_asmt_outcome = connection.get_table('fact_asmt_outcome')

        query = select([dim_asmt.c.asmt_guid,
                        dim_asmt.c.asmt_subject,
                        dim_asmt.c.asmt_type,
                        dim_asmt.c.asmt_period,
                        dim_asmt.c.asmt_version,
                        fact_asmt_outcome.c.asmt_grade],
                       from_obj=[fact_asmt_outcome.join(dim_asmt, fact_asmt_outcome.c.asmt_rec_id == dim_asmt.c.asmt_rec_id)])
        query = query.where(fact_asmt_outcome.c.student_guid == student_guid)
        query = query.order_by(dim_asmt.c.asmt_subject)
        result = connection.get_result(query)
        return result
