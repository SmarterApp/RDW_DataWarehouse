'''
Created on Aug 1, 2013

@author: dawu
'''
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql import select
import json

def get_asmt_custom_metadata(stateCode):
    '''
    Query assessment custom metadata from database
    
    :param string stateCode: state code
    :rtype: dict
    :returns: a dictionary of custom metadata with subject id as key and metadata as its value 
    '''
    asmt_cstm_meta_map = {}
    with SmarterDBConnection() as connector:
        # query custom metadata by state code
        dim_asmt_cstm = connector.get_table(Constants.DIM_ASMT_CUSTOM_METADATA)
        query = select([dim_asmt_cstm.c.asmt_custom_metadata.label(Constants.ASMT_CUSTOM_METADATA),
                        dim_asmt_cstm.c.asmt_subject.label(Constants.ASMT_SUBJECT)],
                       from_obj=[dim_asmt_cstm])\
            .where(dim_asmt_cstm.c.state_code == stateCode)
        results = connector.get_result(query)
        # format by subject
        for result in results:
            custom_metadata = result.get(Constants.ASMT_CUSTOM_METADATA)
            if custom_metadata:
                custom_metadata = json.loads(custom_metadata)
            asmt_cstm_meta_map[result[Constants.ASMT_SUBJECT]] = custom_metadata
    return asmt_cstm_meta_map


def get_subjects_map(asmtSubject=None):
    subjects_map = {}
    # This assumes that we take asmtSubject as optional param
    if asmtSubject is None or (Constants.MATH in asmtSubject and Constants.ELA in asmtSubject):
        subjects_map = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
    elif Constants.MATH in asmtSubject:
            subjects_map = {Constants.MATH: Constants.SUBJECT1}
    elif Constants.ELA in asmtSubject:
            subjects_map = {Constants.ELA: Constants.SUBJECT1}
    return subjects_map

