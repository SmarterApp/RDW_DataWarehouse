__author__ = 'sravi'

from sqlalchemy.sql.expression import and_
from pyramid.threadlocal import get_current_registry

from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants
from smarter.extracts.constants import ExtractType
from smarter.security.context import select_with_context
from smarter_common.security.constants import RolesConstants
from smarter.reports.helpers.filters import apply_filter_to_query


def get_extract_file_chunk_estimate(params, extract_type):
    """
    returns number of extract file chunks that needs to be created based on params and estimate configs
    """
    settings = get_current_registry().settings
    number_of_extract_chunks = int(get_item_raw_extract_size_estimate(params, extract_type) /
                                   int(settings.get('extract.extract_file_chunk_threshold_bytes'))) + 1
    return number_of_extract_chunks


def get_item_raw_extract_size_estimate(params, extract_type):
    """
    private method to generate SQLAlchemy object or sql code to get an estimate for the extract output

    :param params: for query parameters asmt_year, asmt_type, asmt_subject, asmt_grade

    returns approximate estimate (size in bytes) for the extract
    """
    extract_query_record_count = get_extract_record_count(params)
    extract_estimate_file_size = estimate_extract_source_file_size(extract_type)
    return extract_query_record_count * extract_estimate_file_size


def estimate_extract_source_file_size(extract_type):
    """
    returns estimate source file size based on the extract type and configs
    """
    settings = get_current_registry().settings
    if extract_type is ExtractType.itemLevel:
        estimate_file_size = (int(settings.get('extract.estimate.item_level.avg_record_size_bytes')) *
                              int(settings.get('extract.estimate.item_level.avg_record_count'))) + \
                             int(settings.get('extract.estimate.padding_size_bytes'))
    elif extract_type is ExtractType.rawData:
        estimate_file_size = int(settings.get('extract.estimate.raw_data.avg_xml_file_size')) + \
                            int(settings.get('extract.estimate.padding_size_bytes'))
    return estimate_file_size


def get_extract_record_count(params):
    state_code = params.get(Constants.STATECODE)
    asmt_year = params.get(Constants.ASMTYEAR)
    asmt_type = params.get(Constants.ASMTTYPE)
    asmt_subject = params.get(Constants.ASMTSUBJECT)
    asmt_grade = params.get(Constants.ASMTGRADE)

    with EdCoreDBConnection(state_code=state_code) as connector:
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        query = select_with_context([fact_asmt_outcome_vw.c.asmt_outcome_vw_rec_id],
                                    from_obj=[fact_asmt_outcome_vw
                                              .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id))],
                                    permission=RolesConstants.SAR_EXTRACTS,
                                    state_code=state_code)

        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_year == asmt_year))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_type == asmt_type))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_subject == asmt_subject))
        query = query.where(and_(fact_asmt_outcome_vw.c.asmt_grade == asmt_grade))
        query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT))
        query = apply_filter_to_query(query, fact_asmt_outcome_vw, params)  # Filters demographics
        return connector.execute(query).rowcount
