'''
Created on Jun 12, 2015

@author: tosako
'''
from smarter_score_batcher.celery import conf
from smarter_score_batcher.utils.meta import Meta
import json
from smarter_score_batcher.error.exceptions import TSBException
import os
from edcore.database.utils.constants import AssessmentType


def _init_asmt_id_asmt_type():
    '''
    to be efficient use hashmap to lookup asmt_type by subject
    '''
    here = os.path.abspath(os.path.dirname(__file__))
    subject_asmt_type_file = conf.get('smarter_score_batcher.mapping.subject_asmt_type.file', os.path.join(here, '../../../../resources/mapping/subject_asmt_type.json'))
    subject_asmt_type = {}
    path = os.path.abspath(subject_asmt_type_file)
    with open(path) as f:
        json_subject_asmt_type = json.load(f)
        for asmt_type in json_subject_asmt_type.keys():
            subjects = json_subject_asmt_type[asmt_type]
            for subject in subjects:
                subject_asmt_type[subject.upper()] = asmt_type
    return subject_asmt_type


class AIRMeta(Meta):
    '''
    Meta specific to AIR (TIS)
    '''
    subject_asmt_type = _init_asmt_id_asmt_type()

    def __init__(self, valid_meta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date, asmt_id):
        if asmt_type.upper() != AssessmentType.SUMMATIVE:
            asmt_type = self.subject_asmt_type.get(asmt_id.upper())
            if not asmt_type or asmt_type is None:
                '''
                if no asmt_type found, then raise Exception
                '''
                raise TSBAIRUnknownAsmtTypeException('No asmt_type for asmt_id[' + asmt_id + ']')
        super().__init__(valid_meta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date, asmt_id)


class TSBAIRUnknownAsmtTypeException(TSBException):
    def __init__(self, msg):
        TSBException.__init__(self, msg=msg)
