'''
Created on Jun 20, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import select, and_, distinct, func, true
from smarter.trigger.cache.recache import CacheTrigger
from smarter.trigger.database.udl_stats import get_ed_stats
from smarter.reports.helpers.constants import Constants
import logging
from smarter.trigger.utils import run_cron_job
from smarter.trigger.database import constants
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.database.udl_stats_connector import StatsDBConnection


logger = logging.getLogger(__name__)


def prepare_pre_cache(tenant, state_code, last_pre_cached):
    '''
    prepare which state and district are pre-cached

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode representing the state
    :param last_pre_cached:  dateTime of the last precached
    :rType: list
    :return:  list of results containing district guids
    '''
    with SmarterDBConnection(tenant=tenant) as connector:
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select([distinct(fact_asmt_outcome.c.district_guid).label(Constants.DISTRICT_GUID)], from_obj=[fact_asmt_outcome])
        query = query.where(fact_asmt_outcome.c.asmt_create_date > last_pre_cached)
        query = query.where(and_(fact_asmt_outcome.c.state_code == state_code))
        query = query.where(and_(fact_asmt_outcome.c.most_recent == true()))
        results = connector.get_result(query)
        return results


def trigger_precache(tenant, state_code, results):
    '''
    call pre-cache function

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode representing the state
    :param list results:  list of results
    :rType:  boolean
    :returns:  True if precache is triggered and no exceptions are caught
    '''
    triggered = False
    if len(results) > 0:
        triggered = True
        cache_trigger = CacheTrigger(tenant)
        try:
            cache_trigger.recache_state_view_report(state_code)
        except:
            triggered = False
        for result in results:
            try:
                district_guid = result.get(Constants.DISTRICT_GUID)
                cache_trigger.recache_district_view_report(state_code, district_guid)
            except:
                triggered = False
    return triggered


def update_ed_stats_for_precached(tenant, state_code):
    '''
    update current timestamp to last_pre_cached field

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode of the state
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(constants.Constants.UDL_STATS)
        stmt = udl_stats.update(values={udl_stats.c.last_pre_cached: func.now()}).where(udl_stats.c.state_code == state_code).where(udl_stats.c.tenant == tenant)
        connector.execute(stmt)


def precached_task(settings):
    '''
    Precaches reports based on udl stats
    '''
    udl_stats_results = get_ed_stats()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get(constants.Constants.TENANT)
        state_code = udl_stats_result.get(constants.Constants.STATE_CODE)
        last_pre_cached = udl_stats_result.get(constants.Constants.LAST_PRE_CACHED)
        fact_asmt_outcome_results = prepare_pre_cache(tenant, state_code, last_pre_cached)
        triggered_success = trigger_precache(tenant, state_code, fact_asmt_outcome_results)
        if triggered_success:
            update_ed_stats_for_precached(tenant, state_code)


def run_cron_recache(settings):
    '''
    Configure and run cron job to flush and re-cache reports
    '''
    run_cron_job(settings, 'trigger.recache.', precached_task)
