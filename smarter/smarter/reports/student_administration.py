'''
Created on Jan 13, 2013
'''
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_
from edapi.cache import cache_region
from edcore.database.edcore_connector import EdCoreDBConnection


@cache_region('public.shortlived')
def get_student_list_asmt_administration(state_code, district_guid, school_guid, asmt_grade=None, student_guids=None):
    '''
    Get asmt administration for a list of students. There is no PII in the results and it can be stored in shortlived cache
    '''
    with EdCoreDBConnection() as connection:
        fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
        #  should it be always for summative?
        query = select([fact_asmt_outcome.c.asmt_year, fact_asmt_outcome.c.asmt_subject, fact_asmt_outcome.c.asmt_type,
                        fact_asmt_outcome.c.date_taken],
                       from_obj=[fact_asmt_outcome])
        query = query.where(fact_asmt_outcome.c.state_code == state_code).\
                  where(and_(fact_asmt_outcome.c.school_guid == school_guid)).\
                  where(and_(fact_asmt_outcome.c.district_guid == district_guid)).\
                  group_by(fact_asmt_outcome.c.asmt_year, fact_asmt_outcome.c.asmt_subject, fact_asmt_outcome.c.asmt_type, fact_asmt_outcome.c.date_taken).\
                  order_by(fact_asmt_outcome.c.asmt_type.desc(), fact_asmt_outcome.c.date_taken.desc())
        if (asmt_grade is not None):
            query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
        if (student_guids is not None):
            query = query.where(and_(fact_asmt_outcome.c.student_guid.in_(student_guids)))
        x = connection.get_result(query)
        return x
