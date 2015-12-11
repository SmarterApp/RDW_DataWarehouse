from edapi.logging import audit_event
from edapi.decorators import public_report_config, user_info
from edcore.utils.utils import merge_dict
from smarter.reports.helpers.constants import Constants
from smarter.reports.helpers.filters import FILTERS_CONFIG
from smarter.security.context import get_current_request_context
from smarter.reports.compare_pop_report import get_report, REPORT_NAME
from smarter.utils.encryption import decode
import pyramid.threadlocal


EDWARE_PUBLIC_SECRET = 'edware.public.secret'
REPORT_PARAMS = merge_dict({Constants.SID: {"type": "string",
                                            "required": True,
                                            "pattern": "^[a-zA-Z0-9\-\=\_]{20,52}$"},
                            Constants.DISTRICTGUID: {"type": "string",
                                                     "required": False,
                                                     "pattern": "^[a-zA-Z0-9\-]{0,40}$"},
                            Constants.SCHOOLGUID: {"type": "string",
                                                   "required": False,
                                                   "pattern": "^[a-zA-Z0-9\-]{0,40}$"},
                            Constants.ASMTYEAR: {"type": "integer",
                                                 "required": False,
                                                 "pattern": "^[1-9][0-9]{3}$"}
                            }, FILTERS_CONFIG)

SHORT_URL_REPORT_PARAMS = {Constants.SID: {"type": "string",
                                           "required": True,
                                           "pattern": "^[a-zA-Z0-9\-\=\_]{20,52}$"}}


@public_report_config(
    name=REPORT_NAME,
    params=REPORT_PARAMS)
@user_info
@get_current_request_context
@audit_event()
def get_public_comparing_populations_report(params):
    '''
    End point to public comparing populiations report
    '''
    secret_key = pyramid.threadlocal.get_current_registry().settings.get(EDWARE_PUBLIC_SECRET)
    sid = params.pop(Constants.SID)
    params[Constants.STATECODE] = decode(secret_key, sid)
    report = get_report(params, is_public=True)
    report = mask_state_code(report, sid)
    report = mask_breadcrumb(report, sid)
    return report


def mask_state_code(report, sid):
    '''
    mask stateCode to sid
    '''
    records = report.pop(Constants.RECORDS)
    for record in records:
        params = record[Constants.PARAMS]
        params.pop(Constants.STATECODE, None)
        params[Constants.SID] = sid
        record[Constants.PARAMS] = params
    report[Constants.RECORDS] = records
    return report


def mask_breadcrumb(report, sid):
    '''
    mask breadcrumb url
    '''
    for item in report[Constants.CONTEXT][Constants.ITEMS]:
        if Constants.ID in item and item[Constants.TYPE] == Constants.STATE:
            item[Constants.ID] = sid
    return report


@public_report_config(
    name='public_short_url',
    params=SHORT_URL_REPORT_PARAMS)
def create_public_report_short_url(params):
    return "/assets/html/comparingPopulations.html?isPublic=true&sid={}".format(params['sid'])
