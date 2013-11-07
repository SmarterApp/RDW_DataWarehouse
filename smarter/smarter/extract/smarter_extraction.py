'''
Created on Nov 1, 2013

@author: ejen
'''
from edcore.database.edcore_connector import EdCoreDBConnection
from sqlalchemy.sql.expression import and_
from smarter.reports.helpers.constants import Constants, AssessmentType
from smarter.security.context import select_with_context
from psycopg2.extensions import adapt as sqlescape


def bind_sqlalchemy_vars(unbound_sql_code, params):
    '''
    This function bind sqlalchemy sql expression's free variable with its params
    :param unbound_sql_code: a sqlalchemy object
    :param params: dictionary of free variables and their values
    '''
    escaped_params = {}
    for k, v in params.items():
        unbound_sql_code = unbound_sql_code.replace(':' + k, str(sqlescape(v)))

    return unbound_sql_code


def get_extract_assessment_query(params, limit=None, compiled=False):
    """
    private method to generate SQLAlchemy object or sql code for extraction

    :param params: for query parameters asmt_type, asmt_subject, asmt_year, limit, most_recent
    :param limit: for set up limit of result
    :param compile: True to return SQL code, otherwise just SQLALchemy object
    """
    asmt_type = params.get(Constants.ASMTTYPE, None)
    asmt_subject = params.get(Constants.ASMTSUBJECT, None)
    asmt_year = params.get(Constants.ASMTYEAR, 2015)
    state_code = params.get(Constants.STATECODE)
    most_recent = params.get(Constants.MOST_RECENT, True)

    # TODO, can we execute the query here?

    with EdCoreDBConnection() as connector:
        # get handle to tables
        dim_student = connector.get_table(Constants.DIM_STUDENT)
        dim_staff = connector.get_table(Constants.DIM_STAFF)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        # TODO:  Do we really need this? just return None if any of those params are None, and handle it in caller
        # if no subject, and asmt_subject, no state_code or asmt_year, a query should return 0 rows
        # because nothing should be found. should check more before really execute those
        # useless query
        if asmt_type is None or asmt_subject is None or state_code is None or asmt_year is None:
            query = select_with_context([fact_asmt_outcome.c.asmnt_outcome_rec_id.label('asmnt_outcome_rec_id')],
                                        from_obj=[fact_asmt_outcome])
            query = query.where(fact_asmt_outcome.c.asmt_year == 0)
            query = query.limit(0)
        else:
            query = select_with_context([dim_student.c.student_guid.label('student_guid'),
                                        dim_student.c.first_name.label('student_first_name'),
                                        dim_student.c.middle_name.label('student_middle_name'),
                                        dim_student.c.last_name.label('student_last_name'),
                                        dim_inst_hier.c.district_name.label('district_name'),
                                        dim_inst_hier.c.school_name.label('school_name'),
                                        fact_asmt_outcome.c.enrl_grade.label('enrollment_grade'),
                                        dim_staff.c.first_name.label('teacher_first_name'),
                                        dim_staff.c.middle_name.label('teacher_middle_name'),
                                        dim_staff.c.last_name.label('teacher_last_name'),
                                        fact_asmt_outcome.c.asmt_grade.label('asmt_grade'),
                                        dim_asmt.c.asmt_subject.label('asmt_subject'),
                                        fact_asmt_outcome.c.asmt_score.label('asmt_score'),
                                        fact_asmt_outcome.c.asmt_score_range_min.label('asmt_score_range_min'),
                                        fact_asmt_outcome.c.asmt_score_range_max.label('asmt_score_range_max'),
                                        fact_asmt_outcome.c.asmt_perf_lvl.label('asmt_perf_lvl'),
                                        dim_asmt.c.asmt_type.label('asmt_type'),
                                        dim_asmt.c.asmt_score_min.label('asmt_score_min'),
                                        dim_asmt.c.asmt_score_max.label('asmt_score_max'),
                                        dim_asmt.c.asmt_claim_1_name.label('asmt_claim_1_name'),
                                        dim_asmt.c.asmt_claim_2_name.label('asmt_claim_2_name'),
                                        dim_asmt.c.asmt_claim_3_name.label('asmt_claim_3_name'),
                                        dim_asmt.c.asmt_claim_4_name.label('asmt_claim_4_name'),
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
                                        fact_asmt_outcome.c.asmt_claim_4_score_range_max.label('asmt_claim_4_score_range_max')],
                                        from_obj=[fact_asmt_outcome
                                                  .join(dim_student, and_(dim_student.c.student_guid == fact_asmt_outcome.c.student_guid,
                                                                          #dim_student.c.most_recent,
                                                                          dim_student.c.section_guid == fact_asmt_outcome.c.section_guid))
                                                  .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id,
                                                                       dim_asmt.c.asmt_type.in_([AssessmentType.SUMMATIVE, AssessmentType.COMPREHENSIVE_INTERIM])))
                                                  .join(dim_staff, and_(dim_staff.c.staff_guid == fact_asmt_outcome.c.teacher_guid,
                                                                        dim_staff.c.most_recent, dim_staff.c.section_guid == fact_asmt_outcome.c.section_guid))
                                                  .join(dim_inst_hier, and_(dim_inst_hier.c.inst_hier_rec_id == fact_asmt_outcome.c.inst_hier_rec_id))])

            query = query.where(fact_asmt_outcome.c.asmt_type == asmt_type)
            query = query.where(and_(fact_asmt_outcome.c.asmt_subject == asmt_subject))
            query = query.where(and_(fact_asmt_outcome.c.most_recent == most_recent))
            query = query.where(and_(fact_asmt_outcome.c.asmt_year == asmt_year))
            query = query.where(and_(fact_asmt_outcome.c.state_code == state_code))
            if limit is not None:
                query = query.limit(limit)

            if compiled:
                query = bind_sqlalchemy_vars(str(query), query.compile().params)

        return query
