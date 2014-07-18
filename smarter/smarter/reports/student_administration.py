'''
Created on Jan 13, 2013
'''
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_, distinct
from edapi.cache import cache_region
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants, AssessmentType

DEFAULT_YEAR_BACK = 1


def get_student_list_asmt_administration(state_code, district_id, school_id, asmt_grade=None, student_ids=None, asmt_year=None):
    '''
    Get asmt administration for a list of students. There is no PII in the results and it can be stored in shortlived cache
    '''
    with EdCoreDBConnection(state_code=state_code) as connection:
        fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        dim_asmt = connection.get_table(Constants.DIM_ASMT)
        query = select([dim_asmt.c.effective_date, fact_asmt_outcome_vw.c.asmt_type, fact_asmt_outcome_vw .c.asmt_grade],
                       from_obj=[fact_asmt_outcome_vw, dim_asmt])
        query = query.where(fact_asmt_outcome_vw.c.asmt_rec_id == dim_asmt.c.asmt_rec_id).\
            where(fact_asmt_outcome_vw.c.state_code == state_code).\
            where(and_(fact_asmt_outcome_vw.c.school_id == school_id)).\
            where(and_(fact_asmt_outcome_vw.c.district_id == district_id)).\
            where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT)).\
            where(and_(fact_asmt_outcome_vw.c.asmt_type.in_([AssessmentType.SUMMATIVE, AssessmentType.INTERIM_COMPREHENSIVE]))).\
            group_by(dim_asmt.c.effective_date, fact_asmt_outcome_vw.c.asmt_type, fact_asmt_outcome_vw.c.asmt_grade,).\
            order_by(fact_asmt_outcome_vw.c.asmt_type.desc(), dim_asmt.c.effective_date.desc())
        if asmt_grade:
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == asmt_grade))
        if student_ids:
            query = query.where(and_(fact_asmt_outcome_vw.c.student_id.in_(student_ids)))
        if asmt_year:
            query = query.where(and_(fact_asmt_outcome_vw.c.asmt_year == asmt_year))
        results = connection.get_result(query)
    return results


def get_student_report_asmt_administration(state_code, student_id):
    '''
    Get asmt administration for an individual student report. There is no PII in the results and it can be stored in
    shortlived cache
    '''
    with EdCoreDBConnection(state_code=state_code) as connection:
        fact_asmt_outcome_vw = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        dim_asmt = connection.get_table(Constants.DIM_ASMT)
        query = select([dim_asmt.c.effective_date, fact_asmt_outcome_vw.c.asmt_type, fact_asmt_outcome_vw .c.asmt_grade],
                       from_obj=[fact_asmt_outcome_vw, dim_asmt])
        query = query.where(fact_asmt_outcome_vw.c.asmt_rec_id == dim_asmt.c.asmt_rec_id).\
            where(fact_asmt_outcome_vw.c.state_code == state_code).\
            where(and_(fact_asmt_outcome_vw.c.student_id == student_id)).\
            where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT)).\
            group_by(dim_asmt.c.effective_date, fact_asmt_outcome_vw.c.asmt_type, fact_asmt_outcome_vw.c.asmt_grade,).\
            order_by(fact_asmt_outcome_vw.c.asmt_type.desc(), dim_asmt.c.effective_date.desc())
        results = connection.get_result(query)
    return results


@cache_region('public.shortlived')
def get_asmt_academic_years(state_code, tenant=None, years_back=None):
    '''
    Gets academic years.
    '''
    if not years_back or years_back <= 0:
        years_back = DEFAULT_YEAR_BACK
    with EdCoreDBConnection(tenant=tenant, state_code=state_code) as connection:
        dim_asmt = connection.get_table(Constants.DIM_ASMT)
        query = select([dim_asmt.c.asmt_period_year]).distinct().order_by(dim_asmt.c.asmt_period_year.desc())
        results = connection.execute(query).fetchmany(size=years_back)
    return list(r[Constants.ASMT_PERIOD_YEAR] for r in results)


@cache_region('public.shortlived')
def get_student_reg_academic_years(state_code, tenant=None):
    with EdCoreDBConnection(tenant=tenant, state_code=state_code) as connection:
        student_reg = connection.get_table(Constants.STUDENT_REG)
        query = select([distinct(student_reg.c.academic_year).label(Constants.ACADEMIC_YEAR)])\
            .where(student_reg.c.state_code == state_code).order_by(student_reg.c.academic_year.desc())
        results = connection.get_result(query)
    return list(result[Constants.ACADEMIC_YEAR] for result in results)


def get_default_asmt_academic_year(params):
    '''
    Get latest academic year by state code as default.
    '''
    state_code = params.get(Constants.STATECODE)
    return get_asmt_academic_years(state_code)[0]


def set_default_year_back(year_back):
    '''
    Set default year back.
    '''
    if not year_back:
        return
    global DEFAULT_YEAR_BACK
    DEFAULT_YEAR_BACK = int(year_back)
