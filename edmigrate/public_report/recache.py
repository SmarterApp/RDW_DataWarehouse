# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Nov 17, 2015

@author: tosako
'''
from smarter.trigger.cache.recache import CacheTrigger
from edmigrate.database.migrate_public_connector import EdMigratePublicConnection
from smarter.reports.helpers.constants import Constants
from sqlalchemy.sql.expression import distinct, select, and_
import logging

logger = logging.getLogger('edmigrate')


def trigger_public_report_precache(public_tenant, filter_config):
    prev_state_code = None
    prev_district_id = None
    prev_school_id = None
    results = prepare_pre_cache(public_tenant)
    for result in results:
        state_code = result[Constants.STATE_CODE]
        if state_code != prev_state_code:
            cache_trigger = CacheTrigger(public_tenant, state_code, filter_config, is_public=True)
            prev_state_code = state_code
            prev_district_id = None
            prev_school_id = None
            try:
                cache_trigger.recache_cpop_report()
            except Exception as e:
                logger.warning('Recache of state view threw exception for %s', state_code)
                logger.error('Error occurs when recache state view: %s', e)
        district_id = result[Constants.DISTRICT_ID]
        if district_id != prev_district_id:
            prev_district_id = district_id
            prev_school_id = None
            try:
                cache_trigger.recache_cpop_report(district_id=district_id)
            except Exception as e:
                logger.warning('Recache of district view threw exception for state_code %s district_id %s', state_code, district_id)
                logger.error('Error occurs when recache district view: %s', e)
        school_id = result[Constants.SCHOOL_ID]
        if school_id != prev_school_id:
            prev_school_id = school_id
            try:
                cache_trigger.recache_cpop_report(district_id=district_id, school_id=school_id)
            except Exception as e:
                logger.warning('Recache of district view threw exception for state_code %s district_id %s school_id %s', state_code, district_id, school_id)
                logger.error('Error occurs when recache district view: %s', e)


def prepare_pre_cache(public_tenant):
    '''
    prepare which state and district are pre-cached

    :param string tenant:  name of the tenant
    :rType: list
    :return:  list of results containing state_code
    '''
    with EdMigratePublicConnection(public_tenant) as connector:
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        fact_block_asmt_outcome = connector.get_table(Constants.FACT_BLOCK_ASMT_OUTCOME)
        query_fao = select([distinct(fact_asmt_outcome_vw.c.state_code).label(Constants.STATE_CODE),
                            fact_asmt_outcome_vw.c.district_id.label(Constants.DISTRICT_ID),
                            fact_asmt_outcome_vw.c.school_id.label(Constants.SCHOOL_ID)], from_obj=[fact_asmt_outcome_vw])
        query_fao = query_fao.where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT))
        query_fbao = select([distinct(fact_block_asmt_outcome.c.state_code).label(Constants.STATE_CODE),
                             fact_block_asmt_outcome.c.district_id.label(Constants.DISTRICT_ID),
                             fact_block_asmt_outcome.c.school_id.label(Constants.SCHOOL_ID)], from_obj=[fact_block_asmt_outcome])
        query_fbao = query_fbao.where(and_(fact_block_asmt_outcome.c.rec_status == Constants.CURRENT))
        query = query_fao.union(query_fbao).order_by(Constants.STATE_CODE, Constants.DISTRICT_ID, Constants.SCHOOL_ID)
        results = connector.get_result(query)
        return results
