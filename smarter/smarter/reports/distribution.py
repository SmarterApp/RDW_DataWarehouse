'''
Created on Jan 13, 2013
'''
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import label, case
from smarter.reports.helpers.constants import Constants, AssessmentType
from edapi.cache import cache_region
from sqlalchemy.sql.functions import count
from edcore.database.edcore_connector import EdCoreDBConnection

BUCKET_SIZE = 20


@cache_region('public.data')
def get_summary_distribution(state_code, district_guid=None, school_guid=None, asmt_type=AssessmentType.SUMMATIVE):
    '''
    Get a bucketed distribution of scores
    '''
    with EdCoreDBConnection(state_code=state_code) as connection:
        fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
        #  should it be always for summative?
        query = select([label(Constants.SCORE_BUCKET, (fact_asmt_outcome.c.asmt_score / get_bucket_size()) * get_bucket_size()),
                        count(case([(fact_asmt_outcome.c.asmt_subject == Constants.MATH, 1)], else_=0)).label(Constants.TOTAL_MATH),
                        count(case([(fact_asmt_outcome.c.asmt_subject == Constants.ELA, 1)], else_=0)).label(Constants.TOTAL_ELA)],
                       from_obj=[fact_asmt_outcome])
        query = query.where(fact_asmt_outcome.c.state_code == state_code)
        query = query.where(fact_asmt_outcome.c.asmt_type == asmt_type)
        query = query.where(fact_asmt_outcome.c.most_recent)
        query = query.where(fact_asmt_outcome.c.status == 'C')
        if (district_guid is not None):
            query = query.where(fact_asmt_outcome.c.district_guid == district_guid)
        if (school_guid is not None):
            query = query.where(fact_asmt_outcome.c.school_guid == school_guid)
        query = query.group_by(Constants.SCORE_BUCKET).order_by(Constants.SCORE_BUCKET)
        return connection.get_result(query)


def get_bucket_size():
    return BUCKET_SIZE
