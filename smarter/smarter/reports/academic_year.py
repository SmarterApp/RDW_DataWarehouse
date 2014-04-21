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
