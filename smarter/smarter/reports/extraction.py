'''
Created on Jan 24, 2013

@author: tosako
'''
from edcore.database.edcore_connector import EdCoreDBConnection
from sqlalchemy.sql.expression import Select, and_
from sqlalchemy.sql import compiler
from edapi.logging import audit_event
from smarter.reports.helpers.constants import Constants, AssessmentType
from smarter.security.context import select_with_context

def get_extract_query(params):
    """
    """
    asmt_type = params.get(Constants.ASMT_TYPE, None)
    asmt_subject = params.get(Constants.ASMT_SUBJECT, None)
    asmt_year = params.get(Constants.ASMT_YEAR, None)
    limit = params.get(Constants.LIMIT, None)
    most_recent = params.get(Constants.MOST_RECENT, true)

    with EdCoreDBConnection() as connector:
        # get handle to tables
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        # if no subject, and asmt_subject, a query should be 0 because nothing should be found. should check more
        # before really execute those useless query
        if asmt_type is None or asmt_subject is None:
            query = select_with_context([fact_asmt_outcome.c.asmnt_outcome_rec_id.label('asmnt_outcome_rec_id')],
                                        from_obj=[fact_asmt_outcome])
            query = query.where(fact_asmt_outcome.c.asmt_year == 0)
            query = query.limit(0)
        else:
            query = select_with_context([fact_asmt_outcome.c.asmnt_outcome_rec_id.label('asmnt_outcome_rec_id')],
                                        from_obj=[fact_asmt_outcome])

            query = query.where(fact_asmt_outcome.c.asmt_type == asmt_type)
            query = query.where(and_(fact_asmt_outcome.c.asmt_subject == asmt_subject))
            query = query.where(and_(fact_asmt_outcome.c.most_recent == most_recent))
            if limit is not None:
                query = query.limit(limit)

        return query


def get_check_ela_interim_existence_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.COMPREHENSIVE_INTERIM,
                             Constants.ASMT_SUBJECT: Constants.ELA,
                             Constatns.LIMIT: 1})


def get_check_ela_summative_existence_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.SUMMATIVE,
                             Constants.ASMT_SUBJECT: Constants.ELA,
                             Constatns.LIMIT: 1})


def get_check_math_interim_existence_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.COMPREHENSIVE_INTERIM,
                             Constants.ASMT_SUBJECT: Constants.MATH,
                             Constatns.LIMIT: 1})


def get_check_math_summative_existence_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.SUMMATIVE,
                             Constants.ASMT_SUBJECT: Constants.MATH,
                             Constatns.LIMIT: 1})


def get_ela_interim_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.COMPREHENSIVE_INTERIM,
                             Constants.ASMT_SUBJECT: Constants.ELA})


def get_ela_summative_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.SUMMATIVE,
                             Constants.ASMT_SUBJECT: Constants.ELA,
                             Constatns.LIMIT: 1})


def get_math_interim_query(asmt_year):
    """
    """
    return get_extract_query({Constants.ASMT_TYPE: AssessmentType.COMPREHENSIVE_INTERIM,
                                          Constants.ASMT_SUBJECT: Constants.MATH,
                                          Constatns.LIMIT: 1})


def get_math_summative_query(asmt_year):
    """
    """
    return get_check_data_existence_query({Constants.ASMT_TYPE: AssessmentType.SUMMATIVE,
                                          Constants.ASMT_SUBJECT: Constants.MATH,
                                          Constatns.LIMIT: 1})
