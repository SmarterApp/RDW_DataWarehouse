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
Created on Jun 23, 2013

@author: tosako
'''
import logging

from sqlalchemy.sql.expression import select, and_, func, null, distinct

from edcore.database.stats_connector import StatsDBConnection
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.database.utils.constants import UdlStatsConstants
from edcore.utils.utils import run_cron_job
from edcore.security.tenant import get_tenant_map

from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_absolute_file_path_name
from smarter.reports.helpers.constants import Constants

from batch.pdf.pdf_generator import PDFGenerator


logger = logging.getLogger('smarter')


def prepare_ed_stats():
    '''
    Get stats data to determine data that has not generated a pdf
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = select([udl_stats.c.rec_id.label(UdlStatsConstants.REC_ID),
                        udl_stats.c.tenant.label(UdlStatsConstants.TENANT),
                        udl_stats.c.load_start.label(UdlStatsConstants.LOAD_START),
                        udl_stats.c.load_end.label(UdlStatsConstants.LOAD_END),
                        udl_stats.c.record_loaded_count.label(UdlStatsConstants.RECORD_LOADED_COUNT),
                        udl_stats.c.batch_guid.label(UdlStatsConstants.BATCH_GUID)],
                       from_obj=[udl_stats])
        query = query.where(udl_stats.c.load_status == UdlStatsConstants.MIGRATE_INGESTED)
        query = query.where(and_(udl_stats.c.last_pdf_task_requested == null()))
        return connector.get_result(query)


def prepare_pre_pdf(tenant, state_code, batch_guid):
    '''
    prepare which state and district are pre-cached

    :param string tenant: name of the tenant
    :param string state_code: stateCode representing the state
    :param string batch_guid: batch GUID
    :rType: list
    :return:  list of results containing student information used to generate pdf
    '''
    with EdCoreDBConnection(tenant=tenant) as connector:
        fact_asmt_outcome_vw = connector.get_table(Constants.FACT_ASMT_OUTCOME_VW)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        query = select([distinct(fact_asmt_outcome_vw.c.student_id).label(Constants.STUDENT_ID),
                        dim_asmt.c.asmt_period_year.label(Constants.ASMT_PERIOD_YEAR),
                        fact_asmt_outcome_vw.c.date_taken.label(Constants.DATETAKEN),
                        dim_asmt.c.asmt_type.label(Constants.ASMT_TYPE),
                        fact_asmt_outcome_vw.c.district_id.label(Constants.DISTRICT_ID),
                        fact_asmt_outcome_vw.c.school_id.label(Constants.SCHOOL_ID),
                        fact_asmt_outcome_vw.c.asmt_grade.label(Constants.ASMT_GRADE)],
                       from_obj=[fact_asmt_outcome_vw
                                 .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome_vw.c.asmt_rec_id,
                                                      dim_asmt.c.rec_status == Constants.CURRENT))])
        query = query.where(fact_asmt_outcome_vw.c.state_code == state_code)
        query = query.where(and_(fact_asmt_outcome_vw.c.batch_guid == batch_guid))
        query = query.where(and_(fact_asmt_outcome_vw.c.rec_status == Constants.CURRENT))
        results = connector.get_result(query)
        return results


def trigger_pre_pdf(settings, state_code, tenant, results):
    '''
    call pre-pdf function

    :param dict settings: application configuration
    :param string tenant: name of the tenant
    :param string state_code: stateCode representing the state
    :param list results: list of results
    :rType: boolean
    :returns: True if pdf generation is triggered and no exceptions are caught
    '''
    if not results:
        return False

    logger.info('trigger_pre_pdf has [%d] results to process for [%s] tenant', len(results), tenant)

    triggered = True
    base_dir = settings.get('pdf.report_base_dir', '/tmp')
    pdf_trigger = PDFGenerator(settings, tenant)
    for result in results:
        student_id = result.get(Constants.STUDENT_ID)
        asmt_period_year = str(result.get(Constants.ASMT_PERIOD_YEAR))
        district_id = result.get(Constants.DISTRICT_ID)
        school_id = result.get(Constants.SCHOOL_ID)
        asmt_grade = result.get(Constants.ASMT_GRADE)
        date_taken = result.get(Constants.DATETAKEN)
        asmt_type = result.get(Constants.ASMT_TYPE)
        file_name = generate_isr_absolute_file_path_name(pdf_report_base_dir=base_dir,
                                                         state_code=state_code,
                                                         asmt_period_year=asmt_period_year,
                                                         district_id=district_id,
                                                         school_id=school_id,
                                                         asmt_grade=asmt_grade,
                                                         student_id=student_id,
                                                         asmt_type=asmt_type,
                                                         grayScale=True,
                                                         date_taken=date_taken)

        logger.debug('pre-pdf for [%s]', file_name)
        logger.info('Generating pdf for student #%s', student_id)
        try:
            pdf_trigger.send_pdf_request(student_id, state_code, asmt_period_year, asmt_type, date_taken, file_name)
        except Exception:
            triggered = False
            logger.warning('Pdf generation failed for student #%s with following error', student_id, exc_info=True)

    return triggered


def update_ed_stats_for_prepdf(rec_id):
    '''
    Sets current timestamp to the `last_pdf_generated` field for row with
    specified `rec_id`

    :param rec_id: record id
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        connector.execute(udl_stats
                          .update(values={udl_stats.c.last_pdf_task_requested: func.now()})
                          .where(udl_stats.c.rec_id == rec_id))


def prepdf_task(settings):
    '''
    Generates pdfs for students that have new assessments

    :param dict settings: configuration for the application
    '''
    logger.info('Running prepdf_task...')
    udl_stats_results = prepare_ed_stats()
    logger.info('Received %s rows from ed stats to process', len(udl_stats_results))
    tenant_to_state_code = get_tenant_map()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get(UdlStatsConstants.TENANT)
        state_code = tenant_to_state_code.get(tenant)
        batch_guid = udl_stats_result.get(UdlStatsConstants.BATCH_GUID)

        fact_asmt_outcome_vw_results = prepare_pre_pdf(tenant, state_code, batch_guid)
        if not fact_asmt_outcome_vw_results:
            logger.info('No results found for batch_guid %s', batch_guid)
            continue

        logger.info('Triggering pre_pdf for %s', batch_guid)
        triggered_success = trigger_pre_pdf(settings, state_code, tenant, fact_asmt_outcome_vw_results)
        if triggered_success:
            update_ed_stats_for_prepdf(udl_stats_result[UdlStatsConstants.REC_ID])
            logger.info('Successfully wrote last_pdf_task_requested for batch_guid %s', batch_guid)
        else:
            logger.warning('Unsuccessful trigger_pre_pdf for batch_guid %s', batch_guid)


def run_cron_prepdf(settings):
    '''
    Configure and run cron job to regenerate pdfs for students with new assessment data

    :param dict settings: configuration for the application
    '''
    run_cron_job(settings, 'trigger.pdf.', prepdf_task)
