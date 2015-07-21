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

def get_user_close_context(request_params, school_rollup_bound=10, tenant=None):
    '''
    Get user's context relationships
    @request_params query params to infer tenant and state from
    @school_rollup_bound - a threshold of number of schools in a district, over which it should only display district
    '''
    state_code = request_params.get(Constants.STATECODE)
    tenant = tenant if tenant else get_tenant_by_state_code(state_code)
    context = get_user_context_for_role(tenant, RolesConstants.PII, request_params)
    districts = []
    schools = []
    
    def __get_names(distrcit_item, school_id = None):
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
            districts.append(item)
    return {Constants.DISTRICTS: districts, Constants.SCHOOLS: schools}

def get_names(tenant, state_code, district_id, school_id):
    context_name = get_district_level_context_names(tenant, state_code, district_id)
    
    if school_id:
        context_name = context_name[Constants.SCHOOLS].get(school_id, None)
        if not context_name:
            return None
    return {Constants.NAME: context_name[Constants.NAME]}
    

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
                           from_obj=[dim_inst_hier], limit=1)

            query = query.where(and_(dim_inst_hier.c.rec_status == Constants.CURRENT))
            query = query.where(and_(dim_inst_hier.c.state_code == state_code))
            query = query.where(and_(dim_inst_hier.c.district_id == district_id))

            # run it and format the results
            results = connector.get_result(query)
            if results:
                schools = {r[Constants.SCHOOL_ID]: {Constants.NAME: r[Constants.SCHOOL_NAME], Constants.SCHOOLGUID: r[Constants.SCHOOL_ID]} for r in results}
                return {Constants.NAME: results[0][Constants.DISTRICT_NAME], 'schools': schools}
    return {}
                
                