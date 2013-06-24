'''
Created on Jun 20, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import select, and_, distinct, func, true
from database.connector import DBConnection
from smarter.database.datasource import get_datasource_name
from smarter.trigger.cache.recache import CacheTrigger
from smarter.trigger.database.connector import StatsDBConnection
from apscheduler.scheduler import Scheduler
from smarter.trigger.database.udl_stats import get_ed_stats
from smarter.reports.helpers.constants import Constants
import logging


logger = logging.getLogger(__name__)


def prepare_pre_cache(tenant, state_code, last_pre_cached):
    '''
    prepare which state and district are pre-cached
    '''
    with DBConnection(name=get_datasource_name(tenant)) as connector:
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
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table('udl_stats')
        stmt = udl_stats.update(values={udl_stats.c.last_pre_cached: func.now()}).where(udl_stats.c.state_code == state_code).where(udl_stats.c.tenant == tenant)
        connector.execute(stmt)


def precached_task():
    udl_stats_results = get_ed_stats()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get('tenant')
        state_code = udl_stats_result.get('state_code')
        last_pre_cached = udl_stats_result.get('last_pre_cached')
        fact_asmt_outcome_results = prepare_pre_cache(tenant, state_code, last_pre_cached)
        triggered_success = trigger_precache(tenant, state_code, fact_asmt_outcome_results)
        if triggered_success:
            update_ed_stats_for_precached(tenant, state_code)


def run_cron_recache(settings):
    trigger_recache = settings.get("trigger.recache.enable", False)
    if trigger_recache:
        cron_time = {}
        year = settings.get("trigger.recache.schedule.cron.year")
        month = settings.get("trigger.recache.schedule.cron.month")
        day = settings.get("trigger.recache.schedule.cron.day")
        week = settings.get("trigger.recache.schedule.cron.week")
        day_of_week = settings.get("trigger.recache.schedule.cron.day_of_week")
        hour = settings.get("trigger.recache.schedule.cron.hour")
        minute = settings.get("trigger.recache.schedule.cron.minute")
        second = settings.get("trigger.recache.schedule.cron.second")

        if year is not None:
            cron_time['year'] = year
        if month is not None:
            cron_time['month'] = month
        if day is not None:
            cron_time['day'] = day
        if week is not None:
            cron_time['week'] = week
        if day_of_week is not None:
            cron_time['day_of_week'] = day_of_week
        if hour is not None:
            cron_time['hour'] = hour
        if minute is not None:
            cron_time['minute'] = minute
        if second is not None:
            cron_time['second'] = second
        if len(cron_time) > 0:
            sched = Scheduler()
            sched.start()
            logger.info('cron job is added for precached_task')
            sched.add_cron_job(precached_task, **cron_time)
