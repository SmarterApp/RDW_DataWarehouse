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
Created on Apr 17, 2014

@author: tosako
'''
from edapi.decorators import report_config
from smarter.reports.helpers.constants import Constants
from smarter.reports.student_administration import get_student_reg_academic_years,\
    get_asmt_academic_years


@report_config(
    name="academic_year",
    params={
        Constants.STATECODE: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z]{2}$",
        },
    })
def get_academic_years(param):
    state_code = param[Constants.STATECODE]
    return {Constants.STUDENT_REG_ACADEMIC_YEAR: get_student_reg_academic_years(state_code),
            Constants.ASMT_PERIOD_YEAR: get_asmt_academic_years(state_code)}
