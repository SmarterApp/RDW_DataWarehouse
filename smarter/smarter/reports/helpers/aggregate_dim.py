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


def get_aggregate_dim(stateCode=None, districtGuid=None, schoolGuid=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None, subjects={}):
    records = {}
    for subject_key in subjects.keys():
        subject = subjects[subject_key]
        rows = _get_aggregate_dim(stateCode, districtGuid, schoolGuid, asmtType, asmtYear, tenant, subject_key, subject)
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


@cache_region('public.shortlived')
def _get_aggregate_dim(stateCode=None, districtGuid=None, schoolGuid=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None, subject_key=None, subject=None):
    '''
    Query for institution or grades that have asmts for the year provided
    :param string stateCode
    :param string districtGuid
    :param string schoolGuid
    :param string asmtType
    :param string asmtYear
    :param string tenant: tenant info for database connection
    :rtype: rset
    :returns: set of records with district guids
    '''
    rows = {}
    # for key in subjects.keys():
    #    subject = subjects[key]
    with EdCoreDBConnection(tenant=tenant, state_code=stateCode) as connector:
        # query custom metadata by state code
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        s = exists(['*'], from_obj=[dim_inst_hier]).where(and_(fact_asmt_outcome.c.asmt_year == asmtYear, fact_asmt_outcome.c.state_code == stateCode, fact_asmt_outcome.c.rec_status == 'C',
                                                               fact_asmt_outcome.c.asmt_type == asmtType, fact_asmt_outcome.c.inst_hier_rec_id == dim_inst_hier.c.inst_hier_rec_id,
                                                               fact_asmt_outcome.c.asmt_subject == subject))
        if districtGuid is None and schoolGuid is None:
            query = get_select_for_state_view(dim_inst_hier, stateCode).where(s)
        elif districtGuid is not None and schoolGuid is not None:
            query = get_select_for_school_view(fact_asmt_outcome, stateCode, districtGuid, schoolGuid, asmtYear, asmtType, subject)
        else:
            query = get_select_for_district_view(dim_inst_hier, stateCode, districtGuid).where(s)
        results = connector.get_result(query)
        for result in results:
            params = {Constants.ID: result.get(Constants.ID), Constants.STATECODE: stateCode}
            if districtGuid is not None:
                params[Constants.DISTRICTGUID] = districtGuid
            if schoolGuid is not None:
                params[Constants.SCHOOLGUID] = schoolGuid
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
    return select([distinct(dim_inst_hier.c.district_guid).label(Constants.ID), dim_inst_hier.c.district_name.label(Constants.NAME)], from_obj=[dim_inst_hier]).where(dim_inst_hier.c.state_code == state_code)


def get_select_for_district_view(dim_inst_hier, state_code, district_guid):
    return select([distinct(dim_inst_hier.c.school_guid).label(Constants.ID), dim_inst_hier.c.school_name.label(Constants.NAME)], from_obj=[dim_inst_hier])\
        .where(and_(dim_inst_hier.c.state_code == state_code, dim_inst_hier.c.district_guid == district_guid))


def get_select_for_school_view(fact_asmt_outcome, state_code, district_guid, school_guid, asmtYear, asmtType, subject):
    return select([distinct(fact_asmt_outcome.c.asmt_grade).label(Constants.ID), fact_asmt_outcome.c.asmt_grade.label(Constants.NAME)], from_obj=[fact_asmt_outcome])\
        .where(and_(fact_asmt_outcome.c.state_code == state_code,
                    fact_asmt_outcome.c.district_guid == district_guid,
                    fact_asmt_outcome.c.school_guid == school_guid,
                    fact_asmt_outcome.c.asmt_year == asmtYear,
                    fact_asmt_outcome.c.rec_status == 'C',
                    fact_asmt_outcome.c.asmt_type == asmtType,
                    fact_asmt_outcome.c.asmt_subject == subject))
