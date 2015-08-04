'''
Created on Jul 15, 2015

@author: agrebneva
'''
from edapi.cache import cache_region
from smarter.security.context import get_user_context_for_role
from smarter_common.security.constants import RolesConstants
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql import and_, select
from edcore.security.tenant import get_tenant_by_state_code
from edapi.decorators import report_config

REPORT_NAME = 'quick_links'


@report_config(
    name=REPORT_NAME,
    params={
        Constants.STATECODE: {
            "type": "string",
            "required": True,
            "pattern": "^[a-zA-Z]{2}$",
        },
        Constants.QUICK_LINKS_SCHOOL_ROLLUP_BOUND: {
            "type": "integer",
            "required": False,
            "pattern": "^[0-9]*$"
        },
        Constants.QUICK_LINKS_DISTRICT_ROLLUP_BOUND: {
            "type": "integer",
            "required": False,
            "pattern": "^[0-9]*$"
        }
    })
def get_quick_links(params):
    return {'quick_links': get_user_close_context(params,
            district_rollup_bound=params.get(Constants.QUICK_LINKS_DISTRICT_ROLLUP_BOUND, 9),
            school_rollup_bound=params.get(Constants.QUICK_LINKS_SCHOOL_ROLLUP_BOUND, 9))}


def get_user_close_context(request_params, district_rollup_bound=9, school_rollup_bound=9, tenant=None):
    '''
    Get user's context relationships
    @request_params query params to infer tenant and state from
    @school_rollup_bound - a threshold of number of schools in a district, over which it should only display district
    '''
    state_code = request_params.get(Constants.STATECODE)
    tenant = tenant if tenant else get_tenant_by_state_code(state_code)
    context = get_user_context_for_role(tenant, RolesConstants.PII, request_params)
    contextGeneral = get_user_context_for_role(tenant, RolesConstants.GENERAL, request_params)
    contextMap = {x[Constants.DISTRICTGUID]: x for x in context}
    contextGeneralMap = {x[Constants.DISTRICTGUID]: x for x in contextGeneral}
    
    # copy missing schools from general
    for key in contextMap:
        if contextGeneralMap[key]:
            guids = set(contextMap[key][Constants.GUID])
            guids.expand(contextGeneralMap[key][Constants.GUID]) 
            contextMap[key][Constants.GUID] = guids
    context = contextGeneral.update(contextMap.values())        
    
    districts = []
    schools = []

    def __get_names(distrcit_item, school_id=None):
        return get_names(tenant, state_code, x[Constants.DISTRICTGUID], school_id)

    for item in context:
        x = item[Constants.PARAMS]
        context_names = __get_names(x)
        # if found matching institution id in tenant's data
        if context_names:
            close_schools = x.pop(Constants.GUID, None)
            if close_schools:
                if len(close_schools) < school_rollup_bound:
                    for school_id in close_schools:
                        params = {Constants.SCHOOLGUID: school_id}
                        params.update(x)
                        school = {Constants.PARAMS: params}
                        name = __get_names(x, school_id)
                        if name:
                            school.update(name)
                            schools.append(school)
            item.update(context_names)
            if len(context) < district_rollup_bound:
                districts.append(item)
    sorted_schools = sorted(schools, key=lambda school: school['name'])
    sorted_districts = sorted(districts, key=lambda district: district['name'])
    return {Constants.DISTRICTS: sorted_districts[:district_rollup_bound - 1], Constants.SCHOOLS: sorted_schools[:school_rollup_bound - 1]}


def get_names(tenant, state_code, district_id, school_id):
    context_name = get_district_level_context_names(tenant, state_code, district_id)

    if school_id:
        context_name = context_name[Constants.SCHOOLS].get(school_id, None)
        if not context_name:
            return None
    name = context_name.get(Constants.NAME)
    return {Constants.NAME: name} if name is not None else None


@cache_region('public.shortlived')
def get_district_level_context_names(tenant, state_code, district_id):
    if state_code:
        with EdCoreDBConnection(tenant=tenant, state_code=state_code) as connector:
            dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
            # Limit result count to one
            # We limit the results to one since we'll get multiple rows with the same values
            # Think of the case of querying for state name and id, we'll get all the schools in that state
            query = select([dim_inst_hier.c.state_code.label(Constants.STATE_CODE),
                            dim_inst_hier.c.district_id.label(Constants.DISTRICT_ID),
                            dim_inst_hier.c.district_name.label(Constants.DISTRICT_NAME),
                            dim_inst_hier.c.school_name.label(Constants.SCHOOL_NAME),
                            dim_inst_hier.c.school_id.label(Constants.SCHOOL_ID)],
                           from_obj=[dim_inst_hier])

            query = query.where(and_(dim_inst_hier.c.rec_status == Constants.CURRENT))
            query = query.where(and_(dim_inst_hier.c.state_code == state_code))
            query = query.where(and_(dim_inst_hier.c.district_id == district_id))

            # run it and format the results
            results = connector.get_result(query)
            if results:
                schools = {r[Constants.SCHOOL_ID]: {Constants.NAME: r[Constants.SCHOOL_NAME], Constants.SCHOOLGUID: r[Constants.SCHOOL_ID]} for r in results}
                return {Constants.NAME: results[0][Constants.DISTRICT_NAME], 'schools': schools}
    return {}
