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
Created on Jan 24, 2013

@author: tosako
'''

from edapi.decorators import report_config, user_info
from edapi.logging import audit_event
from smarter.reports.helpers.constants import Constants, AssessmentType
from edcore.utils.utils import merge_dict
from smarter.security.tenant import validate_user_tenant
from smarter.reports.helpers.filters import FILTERS_CONFIG
from smarter.security.context import get_current_request_context
from smarter.reports.student_administration import get_default_asmt_academic_year
from smarter.reports.list_of_students_report_fao import get_list_of_students_report_fao
from smarter.reports.list_of_students_report_iab import get_list_of_students_report_iab


REPORT_NAME = "list_of_students"

REPORT_PARAMS = merge_dict({
    Constants.STATECODE: {
        "type": "string",
        "required": True,
        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
    },
    Constants.DISTRICTGUID: {
        "type": "string",
        "required": True,
        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
    },
    Constants.SCHOOLGUID: {
        "type": "string",
        "required": True,
        "pattern": "^[a-zA-Z0-9\-]{0,50}$",
    },
    Constants.ASMTGRADE: {
        "type": "string",
        "maxLength": 2,
        "required": False,
        "pattern": "^[K0-9]+$",
    },
    Constants.ASMTSUBJECT: {
        "type": "array",
        "required": False,
        "items": {
            "type": "string",
            "pattern": "^(" + Constants.ELA + "|" + Constants.MATH + ")$",
        }
    },
    Constants.ASMTYEAR: {
        "type": "integer",
        "required": False,
        "pattern": "^[1-9][0-9]{3}$"
    },
    Constants.ASMTTYPE: {
        "enum": [AssessmentType.INTERIM_ASSESSMENT_BLOCKS, AssessmentType.INTERIM_COMPREHENSIVE, AssessmentType.SUMMATIVE],
        "required": False
    }
}, FILTERS_CONFIG)


@report_config(
    name=REPORT_NAME,
    params=REPORT_PARAMS)
@validate_user_tenant
@user_info
@get_current_request_context
@audit_event()
def get_list_of_students_report(params):
    '''
    List of Students Report
    :param dict params:  dictionary of parameters for List of student report
    '''
    asmtYear = params.get(Constants.ASMTYEAR)
    asmtType = params.get(Constants.ASMTTYPE)
    # set default asmt year
    if not asmtYear:
        asmtYear = get_default_asmt_academic_year(params)
        params[Constants.ASMTYEAR] = asmtYear

    if asmtType is not None and asmtType == AssessmentType.INTERIM_ASSESSMENT_BLOCKS:
        return get_list_of_students_report_iab(params)
    else:
        return get_list_of_students_report_fao(params)
