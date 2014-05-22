'''
Created on Dec 4, 2013

@author: dip
'''
from smarter.reports.helpers.constants import Constants
from edcore.database.edcore_connector import EdCoreDBConnection
from sqlalchemy.sql.expression import select, and_, literal
from smarter.extracts.format import get_column_mapping


def get_metadata_file_name(params):
    '''
    Returns file name of json metadata
    '''
    return "METADATA_ASMT_{asmtYear}_{stateCode}_GRADE_{asmtGrade}_{asmtSubject}_{asmtType}_{asmtGuid}.json".\
        format(stateCode=params.get(Constants.STATECODE).upper(),
               asmtGrade=params.get(Constants.ASMTGRADE).upper(),
               asmtSubject=params.get(Constants.ASMTSUBJECT).upper(),
               asmtType=params.get(Constants.ASMTTYPE).upper(),
               asmtYear=params.get(Constants.ASMTYEAR),
               asmtGuid=params.get(Constants.ASMTGUID))


def get_asmt_metadata(state_code, asmt_guid):
    '''
    Generates a query for getting assessment information based on assessment guid

    :param str asmt_guid:  asessment guid
    '''
    with EdCoreDBConnection(state_code=state_code) as connector:
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        mapping = get_column_mapping(Constants.DIM_ASMT, json_mapping=True)
        query = select([literal("assessment").label("content"),
                        dim_asmt.c.asmt_guid.label(mapping.get('asmt_guid', 'asmt_guid')),
                        dim_asmt.c.asmt_type.label(mapping.get('asmt_type', 'asmt_type')),
                        dim_asmt.c.asmt_period_year.label(mapping.get('asmt_period_year', 'asmt_period_year')),
                        dim_asmt.c.asmt_period.label(mapping.get('asmt_period', 'asmt_period')),
                        dim_asmt.c.asmt_version.label(mapping.get('asmt_version', 'asmt_version')),
                        dim_asmt.c.asmt_subject.label(mapping.get('asmt_subject', 'asmt_subject')),
                        dim_asmt.c.effective_date.label(mapping.get('effective_date', 'effective_date')),
                        dim_asmt.c.asmt_score_min.label(mapping.get('asmt_score_min', 'asmt_score_min')),
                        dim_asmt.c.asmt_score_max.label(mapping.get('asmt_score_max', 'asmt_score_max')),
                        dim_asmt.c.asmt_perf_lvl_name_1.label(mapping.get('asmt_perf_lvl_name_1', 'asmt_perf_lvl_name_1')),
                        dim_asmt.c.asmt_perf_lvl_name_2.label(mapping.get('asmt_perf_lvl_name_2', 'asmt_perf_lvl_name_2')),
                        dim_asmt.c.asmt_perf_lvl_name_3.label(mapping.get('asmt_perf_lvl_name_3', 'asmt_perf_lvl_name_3')),
                        dim_asmt.c.asmt_perf_lvl_name_4.label(mapping.get('asmt_perf_lvl_name_4', 'asmt_perf_lvl_name_4')),
                        dim_asmt.c.asmt_perf_lvl_name_5.label(mapping.get('asmt_perf_lvl_name_5', 'asmt_perf_lvl_name_5')),
                        dim_asmt.c.asmt_cut_point_1.label(mapping.get('asmt_cut_point_1', 'asmt_cut_point_1')),
                        dim_asmt.c.asmt_cut_point_2.label(mapping.get('asmt_cut_point_2', 'asmt_cut_point_2')),
                        dim_asmt.c.asmt_cut_point_3.label(mapping.get('asmt_cut_point_3', 'asmt_cut_point_3')),
                        dim_asmt.c.asmt_cut_point_4.label(mapping.get('asmt_cut_point_4', 'asmt_cut_point_4')),
                        dim_asmt.c.asmt_claim_1_name.label(mapping.get('asmt_claim_1_name', 'asmt_claim_1_name')),
                        dim_asmt.c.asmt_claim_2_name.label(mapping.get('asmt_claim_2_name', 'asmt_claim_2_name')),
                        dim_asmt.c.asmt_claim_3_name.label(mapping.get('asmt_claim_3_name', 'asmt_claim_3_name')),
                        dim_asmt.c.asmt_claim_4_name.label(mapping.get('asmt_claim_4_name', 'asmt_claim_4_name')),
                        dim_asmt.c.asmt_claim_1_score_min.label(mapping.get('asmt_claim_1_score_min', 'asmt_claim_1_score_min')),
                        dim_asmt.c.asmt_claim_2_score_min.label(mapping.get('asmt_claim_2_score_min', 'asmt_claim_2_score_min')),
                        dim_asmt.c.asmt_claim_3_score_min.label(mapping.get('asmt_claim_3_score_min', 'asmt_claim_3_score_min')),
                        dim_asmt.c.asmt_claim_4_score_min.label(mapping.get('asmt_claim_4_score_min', 'asmt_claim_4_score_min')),
                        dim_asmt.c.asmt_claim_1_score_max.label(mapping.get('asmt_claim_1_score_max', 'asmt_claim_1_score_max')),
                        dim_asmt.c.asmt_claim_2_score_max.label(mapping.get('asmt_claim_2_score_max', 'asmt_claim_2_score_max')),
                        dim_asmt.c.asmt_claim_3_score_max.label(mapping.get('asmt_claim_3_score_max', 'asmt_claim_3_score_max')),
                        dim_asmt.c.asmt_claim_4_score_max.label(mapping.get('asmt_claim_4_score_max', 'asmt_claim_4_score_max')),
                        dim_asmt.c.asmt_claim_perf_lvl_name_1.label(mapping.get('asmt_claim_perf_lvl_name_1', 'asmt_claim_perf_lvl_name_1')),
                        dim_asmt.c.asmt_claim_perf_lvl_name_2.label(mapping.get('asmt_claim_perf_lvl_name_2', 'asmt_claim_perf_lvl_name_2')),
                        dim_asmt.c.asmt_claim_perf_lvl_name_3.label(mapping.get('asmt_claim_perf_lvl_name_3', 'asmt_claim_perf_lvl_name_3'))],
                       from_obj=[dim_asmt])
        query = query.where(and_(dim_asmt.c.asmt_guid == asmt_guid))
        return query
