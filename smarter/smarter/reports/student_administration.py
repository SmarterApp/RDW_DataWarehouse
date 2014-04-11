'''
Created on Jan 13, 2013
'''
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_
from edapi.cache import cache_region
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants

DEFAULT_YEAR_BACK = 1


def get_student_list_asmt_administration(state_code, district_guid, school_guid, asmt_grade=None, student_guids=None, asmt_year=None):
    '''
    Get asmt administration for a list of students. There is no PII in the results and it can be stored in shortlived cache
    '''
    with EdCoreDBConnection(state_code=state_code) as connection:
        fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
        dim_asmt = connection.get_table(Constants.DIM_ASMT)
        query = select([dim_asmt.c.effective_date, fact_asmt_outcome.c.asmt_type, fact_asmt_outcome .c.asmt_grade],
                       from_obj=[fact_asmt_outcome, dim_asmt])
        query = query.where(fact_asmt_outcome.c.asmt_rec_id == dim_asmt.c.asmt_rec_id).\
            where(fact_asmt_outcome.c.state_code == state_code).\
            where(and_(fact_asmt_outcome.c.school_guid == school_guid)).\
            where(and_(fact_asmt_outcome.c.district_guid == district_guid)).\
            where(and_(fact_asmt_outcome.c.rec_status == Constants.CURRENT)).\
            group_by(dim_asmt.c.effective_date, fact_asmt_outcome.c.asmt_type, fact_asmt_outcome.c.asmt_grade,).\
            order_by(fact_asmt_outcome.c.asmt_type.desc(), dim_asmt.c.effective_date.desc())
        if asmt_grade:
            query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
        if student_guids:
            query = query.where(and_(fact_asmt_outcome.c.student_guid.in_(student_guids)))
        if asmt_year:
            query = query.where(and_(fact_asmt_outcome.c.asmt_year == asmt_year))
        results = connection.get_result(query)
    return results


def get_student_report_asmt_administration(state_code, student_guid):
    '''
    Get asmt administration for an individual student report. There is no PII in the results and it can be stored in
    shortlived cache
    '''
    with EdCoreDBConnection(state_code=state_code) as connection:
        fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
        dim_asmt = connection.get_table(Constants.DIM_ASMT)
        query = select([dim_asmt.c.effective_date, fact_asmt_outcome.c.asmt_type, fact_asmt_outcome .c.asmt_grade],
                       from_obj=[fact_asmt_outcome, dim_asmt])
        query = query.where(fact_asmt_outcome.c.asmt_rec_id == dim_asmt.c.asmt_rec_id).\
            where(fact_asmt_outcome.c.state_code == state_code).\
            where(and_(fact_asmt_outcome.c.student_guid == student_guid)).\
            where(and_(fact_asmt_outcome.c.rec_status == Constants.CURRENT)).\
            group_by(dim_asmt.c.effective_date, fact_asmt_outcome.c.asmt_type, fact_asmt_outcome.c.asmt_grade,).\
            order_by(fact_asmt_outcome.c.asmt_type.desc(), dim_asmt.c.effective_date.desc())
        results = connection.get_result(query)
    return results


@cache_region('public.shortlived')
def get_academic_years(state_code, tenant=None, years_back=None):
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


def get_default_academic_year(params):
    '''
    Get latest academic year by state code as default.
    '''
    state_code = params.get(Constants.STATECODE)
    return get_academic_years(state_code)[0]


def set_default_year_back(year_back):
    '''
    Set default year back.
    '''
    if not year_back:
        return
    global DEFAULT_YEAR_BACK
    DEFAULT_YEAR_BACK = int(year_back)
