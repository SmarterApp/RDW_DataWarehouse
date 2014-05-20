'''
Created on May 12, 2014

@author: agrebneva
'''
from sqlalchemy.sql import select, and_, exists
from smarter.reports.helpers.constants import Constants
from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.student_reg_extract_processors.assessment_constants import AssessmentType


def get_aggregate_dim(stateCode=None, districtGuid=None, schoolGuid=None, asmtType=AssessmentType.SUMMATIVE, asmtYear=None, tenant=None):
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
    with EdCoreDBConnection(tenant=tenant, state_code=stateCode) as connector:
        # query custom metadata by state code
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = get_select_for_district_view(dim_inst_hier, stateCode, districtGuid) if districtGuid is not None else get_select_for_state_view(dim_inst_hier, stateCode, districtGuid)
        s = exists(['*'], from_obj=[dim_inst_hier]).where(and_(fact_asmt_outcome.c.asmt_year == asmtYear, fact_asmt_outcome.c.state_code == stateCode, fact_asmt_outcome.c.rec_status == 'C',
                                                               fact_asmt_outcome.c.asmt_type == asmtType, fact_asmt_outcome.c.inst_hier_rec_id == dim_inst_hier.c.inst_hier_rec_id))
        query = query.where(s)
        rows = []
        results = connector.get_result(query)
        for result in results:
            rows.append({Constants.ID: result.get(Constants.ID), Constants.NAME: result.get(Constants.NAME)})
        return {Constants.RECORDS: rows}


def get_select_for_state_view(dim_inst_hier, state_code, district_guid):
    return select([dim_inst_hier.c.district_name.label(Constants.NAME), dim_inst_hier.c.district_guid.label(Constants.ID)], from_obj=[dim_inst_hier]).where(dim_inst_hier.c.state_code == state_code)


def get_select_for_district_view(dim_inst_hier, state_code, district_guid):
    return select([dim_inst_hier.c.school_name.label(Constants.NAME), dim_inst_hier.c.school_guid.label(Constants.ID)], from_obj=[dim_inst_hier])\
        .where(and_(dim_inst_hier.c.state_code == state_code, dim_inst_hier.c.district_guid == district_guid))
