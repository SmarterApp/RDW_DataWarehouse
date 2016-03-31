# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

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


ASMT_TYPE = 'asmt_type'
TEST_LABEL = 'test_label'


def _init_asmt_id_asmt_type():
    '''
    to be efficient use hashmap to lookup asmt_type by subject
    '''
    here = os.path.abspath(os.path.dirname(__file__))
    subject_asmt_type_file = conf.get('smarter_score_batcher.mapping.subject_asmt_type.file', os.path.join(here, '../../../../resources/mapping/testId_asmt_type.json'))
    subject_asmt_type = {}
    path = os.path.abspath(subject_asmt_type_file)
    with open(path) as f:
        json_subject_asmt_type = json.load(f)
        for asmt_type in json_subject_asmt_type.keys():
            testIds = json_subject_asmt_type[asmt_type]
            for testId, testLabel in testIds.items():
                subject_asmt_type[testId.upper()] = {ASMT_TYPE: asmt_type, TEST_LABEL: testLabel}
    return subject_asmt_type


class AIRMeta(Meta):
    '''
    Meta specific to AIR (TIS)
    '''
    subject_asmt_type = _init_asmt_id_asmt_type()

    def __init__(self, valid_meta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date, asmt_id):
        if asmt_type.upper() != AssessmentType.SUMMATIVE:
            asmt = self.subject_asmt_type.get(asmt_id.upper())
            asmt_type = asmt.get(ASMT_TYPE) if asmt is not None else None
            self.testLabel = asmt.get(TEST_LABEL) if asmt is not None else None
            if not asmt_type or asmt_type is None:
                '''
                if no asmt_type found, then raise Exception
                '''
                raise TSBAIRUnknownAsmtTypeException('No asmt_type for asmt_id[' + asmt_id + ']')
        super().__init__(valid_meta, student_id, state_code, district_id, academic_year, asmt_type, subject, grade, effective_date, asmt_id)

    @property
    def test_label(self):
        return self.testLabel


class TSBAIRUnknownAsmtTypeException(TSBException):
    def __init__(self, msg):
        TSBException.__init__(self, msg=msg)
