'''
Created on Jan 13, 2013
'''
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_
from edapi.cache import cache_region
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants


@cache_region('public.shortlived')
def get_student_list_asmt_administration(state_code, district_guid, school_guid, asmt_grade=None, student_guids=None):
    '''
    Get asmt administration for a list of students. There is no PII in the results and it can be stored in shortlived cache
    '''
    with EdCoreDBConnection(state_code=state_code) as connection:
        fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
        dim_asmt = connection.get_table(Constants.DIM_ASMT)
        query = select([fact_asmt_outcome.c.asmt_year, fact_asmt_outcome.c.asmt_type],
                       from_obj=[fact_asmt_outcome, dim_asmt])
        query = query.where(fact_asmt_outcome.c.asmt_rec_id == dim_asmt.c.asmt_rec_id).\
            where(fact_asmt_outcome.c.state_code == state_code).\
            where(and_(fact_asmt_outcome.c.school_guid == school_guid)).\
            where(and_(fact_asmt_outcome.c.district_guid == district_guid)).\
            group_by(fact_asmt_outcome.c.asmt_year, fact_asmt_outcome.c.asmt_type,).\
            order_by(fact_asmt_outcome.c.asmt_type.desc(), fact_asmt_outcome.c.asmt_year.desc())
        if asmt_grade:
            query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
        if student_guids:
            query = query.where(and_(fact_asmt_outcome.c.student_guid.in_(student_guids)))
        results = connection.get_result(query)
    return results
