'''
Created on Jun 20, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import select, and_, distinct, func, true, null
from smarter.trigger.cache.recache import CacheTrigger
import logging
from smarter.trigger.utils import run_cron_job
from smarter.trigger.database import constants
from smarter.database.smarter_connector import SmarterDBConnection
from smarter.database.udl_stats_connector import StatsDBConnection
from smarter.reports.helpers.constants import Constants


logger = logging.getLogger(__name__)


def prepare_ed_stats():
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(constants.Constants.UDL_STATS)
        query = select([udl_stats.c.tenant.label(constants.Constants.TENANT),
                        udl_stats.c.state_code.label(constants.Constants.STATE_CODE),
                        udl_stats.c.load_start.label(constants.Constants.LOAD_START),
                        udl_stats.c.load_end.label(constants.Constants.LOAD_END),
                        udl_stats.c.record_loaded_count.label(constants.Constants.RECORD_LOADED_COUNT),
                        udl_stats.c.batch_guid.label(constants.Constants.BATCH_GUID), ],
                       from_obj=[udl_stats])
        query = query.where(udl_stats.c.load_status == constants.Constants.INGESTED)
        query = query.where(and_(udl_stats.c.last_pre_cached == null()))
        return connector.get_result(query)


def prepare_pre_cache(tenant, state_code, batch_guid):
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
        query = query.where(fact_asmt_outcome.c.state_code == state_code)
        query = query.where(and_(fact_asmt_outcome.c.batch_guid == batch_guid))
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
            logger.warning('Recache of state view threw exception for %s', state_code)
        for result in results:
            try:
                district_guid = result.get(Constants.DISTRICT_GUID)
                cache_trigger.recache_district_view_report(state_code, district_guid)
            except:
                triggered = False
                logger.warning('Recache of district view threw exception for state_code %s district_guid %s', state_code, district_guid)
    return triggered


def update_ed_stats_for_precached(tenant, state_code, batch_guid):
    '''
    update current timestamp to last_pre_cached field

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode of the state
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(constants.Constants.UDL_STATS)
        stmt = udl_stats.update(values={udl_stats.c.last_pre_cached: func.now()}).where(udl_stats.c.state_code == state_code).where(udl_stats.c.tenant == tenant).where(udl_stats.c.batch_guid == batch_guid)
        connector.execute(stmt)


def precached_task(settings):
    '''
    Precaches reports based on udl stats

    :param dict settings:  configuration for the application
    '''
    udl_stats_results = prepare_ed_stats()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get(constants.Constants.TENANT)
        state_code = udl_stats_result.get(constants.Constants.STATE_CODE)
        batch_guid = udl_stats_result.get(constants.Constants.BATCH_GUID)
        fact_asmt_outcome_results = prepare_pre_cache(tenant, state_code, batch_guid)
        triggered_success = trigger_precache(tenant, state_code, fact_asmt_outcome_results)
        if triggered_success:
            update_ed_stats_for_precached(tenant, state_code, batch_guid)


def run_cron_recache(settings):
    '''
    Configure and run cron job to flush and re-cache reports

     :param dict settings:  configuration for the application
    '''
    run_cron_job(settings, 'trigger.recache.', precached_task)
