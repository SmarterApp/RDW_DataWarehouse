'''
Created on May 12, 2014

@author: agrebneva
'''
from sqlalchemy.sql import select, and_, exists
from smarter.reports.helpers.constants import Constants
from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.student_reg_extract_processors.assessment_constants import AssessmentType
from sqlalchemy.sql.expression import distinct
from edapi.cache import cache_region
from copy import deepcopy


def get_aggregate_dim(stateCode=None, districtId=None, schoolId=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None, subjects={}):
    records = {}
    for subject_key in subjects.keys():
        subject = subjects[subject_key]
        rows = _get_aggregate_dim(stateCode, districtId, schoolId, asmtType, asmtYear, tenant, subject_key, subject)
        for key in rows.keys():
            record = records.get(key)
            if record is None:
                records[key] = deepcopy(rows[key])
            else:
                record[Constants.RESULTS][subject_key] = deepcopy(rows[key][Constants.RESULTS][subject_key])
    sorted_records = sorted(list(records.values()), key=lambda k: k['name'])
    for subject_key in subjects.keys():
        for sorted_record in sorted_records:
            results = sorted_record[Constants.RESULTS]
            if results.get(subject_key) is None:
                results[subject_key] = {Constants.ASMT_SUBJECT: subjects[subject_key], Constants.TOTAL: 0, Constants.HASINTERIM: False}
    return {Constants.RECORDS: sorted_records}


def get_aggregate_dim_cache_route(stateCode, districtId, schoolId, asmtType, asmtYear, tenant, subject_key, subject):
    '''
    If school_id is present, return none - do not cache
    '''
    if schoolId is not None:
        return None  # do not cache school level
    return 'public.shortlived'


def get_aggregate_dim_cache_route_cache_key(stateCode, districtId, schoolId, asmtType, asmtYear, tenant, subject_key, subject):
    '''
    Returns cache key for get_aggregate_dim

    :param comparing_pop:  instance of ComparingPopReport
    :returns: a tuple representing a unique key for comparing populations report
    '''
    cache_args = []
    if stateCode is not None:
        cache_args.append(stateCode)
    if districtId is not None:
        cache_args.append(districtId)
    cache_args.append(asmtType)
    cache_args.append(asmtYear)
    cache_args.append(subject)
    return tuple(cache_args)


@cache_region(['public.shortlived'], router=get_aggregate_dim_cache_route, key_generator=get_aggregate_dim_cache_route_cache_key)
def _get_aggregate_dim(stateCode=None, districtId=None, schoolId=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None, subject_key=None, subject=None):
    '''
    Query for institution or grades that have asmts for the year provided
    :param string stateCode
    :param string districtId
    :param string schoolId
    :param string asmtType
    :param string asmtYear
    :param string tenant: tenant info for database connection
    :rtype: rset
    :returns: set of records with district guids
    '''
    rows = {}
    with EdCoreDBConnection(tenant=tenant, state_code=stateCode) as connector:
        # query custom metadata by state code
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        s = exists(['*'], from_obj=[dim_inst_hier]).where(and_(fact_asmt_outcome.c.asmt_year == asmtYear, fact_asmt_outcome.c.state_code == stateCode, fact_asmt_outcome.c.rec_status == 'C',
                                                               fact_asmt_outcome.c.asmt_type == asmtType, fact_asmt_outcome.c.inst_hier_rec_id == dim_inst_hier.c.inst_hier_rec_id,
                                                               fact_asmt_outcome.c.asmt_subject == subject))
        if districtId is None and schoolId is None:
            query = get_select_for_state_view(dim_inst_hier, stateCode).where(s)
        elif districtId is not None and schoolId is not None:
            query = get_select_for_school_view(fact_asmt_outcome, stateCode, districtId, schoolId, asmtYear, asmtType, subject)
        else:
            query = get_select_for_district_view(dim_inst_hier, stateCode, districtId).where(s)
        results = connector.get_result(query)
        for result in results:
            params = {Constants.ID: result.get(Constants.ID), Constants.STATECODE: stateCode}
            if districtId is not None:
                params[Constants.DISTRICTGUID] = districtId
            if schoolId is not None:
                params[Constants.SCHOOLGUID] = schoolId
            data = {Constants.ID: result.get(Constants.ID),
                    Constants.ROWID: result.get(Constants.ID),
                    Constants.NAME: result.get(Constants.NAME),
                    Constants.PARAMS: params,
                    Constants.RESULTS: {}
                    }
            data[Constants.RESULTS][subject_key] = {Constants.ASMT_SUBJECT: subject, Constants.TOTAL: -1, Constants.HASINTERIM: True}
            rows[data[Constants.ID]] = data
    return rows


def get_select_for_state_view(dim_inst_hier, state_code):
    return select([distinct(dim_inst_hier.c.district_id).label(Constants.ID), dim_inst_hier.c.district_name.label(Constants.NAME)], from_obj=[dim_inst_hier]).where(dim_inst_hier.c.state_code == state_code)


def get_select_for_district_view(dim_inst_hier, state_code, district_id):
    return select([distinct(dim_inst_hier.c.school_id).label(Constants.ID), dim_inst_hier.c.school_name.label(Constants.NAME)], from_obj=[dim_inst_hier])\
        .where(and_(dim_inst_hier.c.state_code == state_code, dim_inst_hier.c.district_id == district_id))


def get_select_for_school_view(fact_asmt_outcome, state_code, district_id, school_id, asmtYear, asmtType, subject):
    return select([distinct(fact_asmt_outcome.c.asmt_grade).label(Constants.ID), fact_asmt_outcome.c.asmt_grade.label(Constants.NAME)], from_obj=[fact_asmt_outcome])\
        .where(and_(fact_asmt_outcome.c.state_code == state_code,
                    fact_asmt_outcome.c.district_id == district_id,
                    fact_asmt_outcome.c.school_id == school_id,
                    fact_asmt_outcome.c.asmt_year == asmtYear,
                    fact_asmt_outcome.c.rec_status == 'C',
                    fact_asmt_outcome.c.asmt_type == asmtType,
                    fact_asmt_outcome.c.asmt_subject == subject))
