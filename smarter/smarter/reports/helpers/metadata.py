'''
Created on Aug 1, 2013

@author: dawu
'''
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql import select
import json
from edapi.cache import cache_region
from edcore.database.edcore_connector import EdCoreDBConnection


@cache_region('public.shortlived')
def get_custom_metadata(state_code, tenant=None):
    '''
    Query assessment custom metadata from database

    :param string stateCode: state code
    :param string tenant: tenant info for database connection
    :rtype: dict
    :returns: dict of custom metadata with subject id as key and metadata as its value
    '''
    cstm_meta_map = {}
    min_cell_size = None
    branding = None
    with EdCoreDBConnection(tenant=tenant, state_code=state_code) as connector:
        # query custom metadata by state code
        dim_asmt_cstm = connector.get_table(Constants.CUSTOM_METADATA)
        query = select([dim_asmt_cstm.c.asmt_custom_metadata.label(Constants.ASMT_CUSTOM_METADATA)],
                       from_obj=[dim_asmt_cstm])\
            .where(dim_asmt_cstm.c.state_code == state_code)
        results = connector.get_result(query)
        if results:
            result = results[0]
            custom_metadata = result.get(Constants.ASMT_CUSTOM_METADATA)
            if custom_metadata:
                custom_metadata = json.loads(custom_metadata)
                min_cell_size = custom_metadata.get(Constants.MIN_CELL_SIZE)
                branding = custom_metadata.get(Constants.BRANDING)
                subjects = custom_metadata[Constants.SUBJECTS]
                for subject in subjects:
                    cstm_meta_map[subject] = subjects[subject]
    # format by subject, we will always return a map of colors and minimum cell size
    result = {Constants.BRANDING: branding}
    subject_map = get_subjects_map()
    for key, value in subject_map.items():
        metadata = cstm_meta_map.get(key, {})
        result[value] = {Constants.COLORS: metadata.get(Constants.COLORS), Constants.MIN_CELL_SIZE: min_cell_size}
    return result


def get_subjects_map(asmtSubject=None):
    '''
    Generate subjects mapping based on given assessment subject type.

    :asmtSubject string asmtSubject: assessment subject
    :rtype: dict
    :returns: dict of subjects mapping of given assessment. If subject is None, return all subjects mapping.
    '''
    subjects_map = {}
    # This assumes that we take asmtSubject as optional param
    if asmtSubject is None or (Constants.MATH in asmtSubject and Constants.ELA in asmtSubject):
        subjects_map = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
    elif Constants.MATH in asmtSubject:
            subjects_map = {Constants.MATH: Constants.SUBJECT1}
    elif Constants.ELA in asmtSubject:
            subjects_map = {Constants.ELA: Constants.SUBJECT1}
    return subjects_map
