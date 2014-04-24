'''
Created on Jun 20, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import select, and_, distinct, func, null
from smarter.trigger.cache.recache import CacheTrigger
import logging
from smarter.reports.helpers.constants import Constants
import json
import os
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.database.utils.constants import UdlStatsConstants, LoadType
from edcore.utils.utils import run_cron_job
from edcore.security.tenant import get_tenant_map


logger = logging.getLogger('smarter')


def prepare_ed_stats():
    '''
    Get stats data to determine data that has not been cached
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = select([udl_stats.c.rec_id.label(UdlStatsConstants.REC_ID),
                        udl_stats.c.tenant.label(UdlStatsConstants.TENANT),
                        udl_stats.c.load_start.label(UdlStatsConstants.LOAD_START),
                        udl_stats.c.load_end.label(UdlStatsConstants.LOAD_END),
                        udl_stats.c.record_loaded_count.label(UdlStatsConstants.RECORD_LOADED_COUNT),
                        udl_stats.c.batch_guid.label(UdlStatsConstants.BATCH_GUID), ],
                       from_obj=[udl_stats]).\
            where(and_(udl_stats.c.load_status == UdlStatsConstants.MIGRATE_INGESTED,
                       udl_stats.c.last_pre_cached == null(),
                       udl_stats.c.load_type == LoadType.ASSESSMENT))
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
    with EdCoreDBConnection(tenant=tenant) as connector:
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        query = select([distinct(fact_asmt_outcome.c.district_guid).label(Constants.DISTRICT_GUID)], from_obj=[fact_asmt_outcome])
        query = query.where(fact_asmt_outcome.c.state_code == state_code)
        query = query.where(and_(fact_asmt_outcome.c.batch_guid == batch_guid))
        query = query.where(and_(fact_asmt_outcome.c.rec_status == Constants.CURRENT))
        results = connector.get_result(query)
        return results


def trigger_precache(tenant, state_code, results, filter_config):
    '''
    call pre-cache function

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode representing the state
    :param list results:  list of results
    :rType:  boolean
    :returns:  True if precache is triggered and no exceptions are caught
    '''
    triggered = False
    logger.debug('trigger_precache has [%d] results to process', len(results))
    if len(results) > 0:
        triggered = True
        cache_trigger = CacheTrigger(tenant, state_code, filter_config)
        try:
            logger.debug('pre-caching state[%s]', state_code)
            cache_trigger.recache_state_view_report()
        except Exception as e:
            triggered = False
            logger.warning('Recache of state view threw exception for %s', state_code)
            logger.error('Error occurs when recache state view: %s', e)
        for result in results:
            try:
                district_guid = result.get(Constants.DISTRICT_GUID)
                logger.debug('pre-caching state[%s], district[%s]', state_code, district_guid)
                cache_trigger.recache_district_view_report(district_guid)
            except Exception as e:
                triggered = False
                logger.warning('Recache of district view threw exception for state_code %s district_guid %s', state_code, district_guid)
                logger.error('Error occurs when recache district view: %s', e)
    return triggered


def update_ed_stats_for_precached(rec_id):
    '''
    update current timestamp to last_pre_cached field

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode of the state
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        stmt = udl_stats.update(values={udl_stats.c.last_pre_cached: func.now()}).where(udl_stats.c.rec_id == rec_id)
        connector.execute(stmt)


def precached_task(settings):
    '''
    Precaches reports based on udl stats

    :param dict settings:  configuration for the application
    '''
    filter_settings = read_config_from_json_file(settings.get('trigger.recache.filter.file'))
    udl_stats_results = prepare_ed_stats()
    tenant_to_state_code = get_tenant_map()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get(UdlStatsConstants.TENANT)
        state_code = tenant_to_state_code.get(tenant)
        batch_guid = udl_stats_result.get(UdlStatsConstants.BATCH_GUID)
        fact_asmt_outcome_results = prepare_pre_cache(tenant, state_code, batch_guid)
        triggered_success = trigger_precache(tenant, state_code, fact_asmt_outcome_results, filter_settings)
        if triggered_success:
            update_ed_stats_for_precached(udl_stats_result[UdlStatsConstants.REC_ID])


def run_cron_recache(settings):
    '''
    Configure and run cron job to flush and re-cache reports

     :param dict settings:  configuration for the application
    '''
    run_cron_job(settings, 'trigger.recache.', precached_task)


def read_config_from_json_file(file_name):
    '''
    Read precache filtering setings from .json file

    :param string file_name:  path of json file that contains filters
    '''
    if file_name is None:
        return {}
    abspath = os.path.abspath(file_name)
    if not os.path.exists(abspath):
        raise Exception('File %s not found' % abspath)
    with open(abspath) as file:
        data = json.load(file)
    return data
