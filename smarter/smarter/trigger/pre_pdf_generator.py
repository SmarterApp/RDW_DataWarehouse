'''
Created on Jun 23, 2013

@author: tosako
'''
from sqlalchemy.sql.expression import select, and_, func, true, null, distinct
from batch.pdf.pdf_generator import PDFGenerator
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_absolute_file_path_name
import logging
from smarter.trigger.utils import run_cron_job
from smarter.reports.helpers.constants import Constants, AssessmentType
from edcore.database.stats_connector import StatsDBConnection
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.database.utils.constants import UdlStatsConstants


logger = logging.getLogger('smarter')


def prepare_ed_stats():
    '''
    Get stats data to determine data that has not generated a pdf
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        query = select([udl_stats.c.tenant.label(UdlStatsConstants.TENANT),
                        udl_stats.c.state_code.label(UdlStatsConstants.STATE_CODE),
                        udl_stats.c.load_start.label(UdlStatsConstants.LOAD_START),
                        udl_stats.c.load_end.label(UdlStatsConstants.LOAD_END),
                        udl_stats.c.record_loaded_count.label(UdlStatsConstants.RECORD_LOADED_COUNT),
                        udl_stats.c.batch_guid.label(UdlStatsConstants.BATCH_GUID), ],
                       from_obj=[udl_stats])
        query = query.where(udl_stats.c.load_status == UdlStatsConstants.MIGRATE_INGESTED)
        query = query.where(and_(udl_stats.c.last_pdf_task_requested == null()))
        return connector.get_result(query)


def prepare_pre_pdf(tenant, state_code, batch_guid):
    '''
    prepare which state and district are pre-cached

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode representing the state
    :param last_pdf_generated:  dateTime of the last pdf generated
    :rType: list
    :return:  list of results containing student information used to generate pdf
    '''
    with EdCoreDBConnection(tenant=tenant) as connector:
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        query = select([distinct(fact_asmt_outcome.c.student_guid).label(Constants.STUDENT_GUID),
                        dim_asmt.c.asmt_period_year.label(Constants.ASMT_PERIOD_YEAR),
                        fact_asmt_outcome.c.district_guid.label(Constants.DISTRICT_GUID),
                        fact_asmt_outcome.c.school_guid.label(Constants.SCHOOL_GUID),
                        fact_asmt_outcome.c.asmt_grade.label(Constants.ASMT_GRADE)],
                       from_obj=[fact_asmt_outcome
                                 .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id,
                                                      dim_asmt.c.most_recent,
                                                      dim_asmt.c.asmt_type == AssessmentType.SUMMATIVE))])
        query = query.where(fact_asmt_outcome.c.state_code == state_code)
        query = query.where(and_(fact_asmt_outcome.c.batch_guid == batch_guid))
        query = query.where(and_(fact_asmt_outcome.c.most_recent == true()))
        results = connector.get_result(query)
        return results


def trigger_pre_pdf(settings, state_code, tenant, results):
    '''
    call pre-pdf function

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode representing the state
    :param list results:  list of results
    :rType:  boolean
    :returns:  True if pdf generation is triggered and no exceptions are caught
    '''
    triggered = False
    base_dir = settings.get('pdf.report_base_dir', '/tmp')
    logger.debug('trigger_pre_pdf has [%d] results to process', len(results))
    if len(results) > 0:
        triggered = True
        pdf_trigger = PDFGenerator(settings, tenant)
        for result in results:
            try:
                student_guid = result.get(Constants.STUDENT_GUID)
                asmt_period_year = str(result.get(Constants.ASMT_PERIOD_YEAR))
                district_guid = result.get(Constants.DISTRICT_GUID)
                school_guid = result.get(Constants.SCHOOL_GUID)
                asmt_grade = result.get(Constants.ASMT_GRADE)
                student_guid = result.get(Constants.STUDENT_GUID)
                file_name = generate_isr_absolute_file_path_name(pdf_report_base_dir=base_dir, state_code=state_code, asmt_period_year=asmt_period_year, district_guid=district_guid, school_guid=school_guid, asmt_grade=asmt_grade, student_guid=student_guid)
                logger.debug('pre-pdf for [%s]', file_name)
                pdf_trigger.send_pdf_request(student_guid, state_code, file_name)
            except Exception as e:
                triggered = False
                logger.warning('Pdf generation failed for %s', student_guid)
    return triggered


def update_ed_stats_for_prepdf(tenant, state_code, batch_guid):
    '''
    update current timestamp to last_pdf_generated field

    :param string tenant:  name of the tenant
    :param string state_code:  stateCode of the state
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table(UdlStatsConstants.UDL_STATS)
        stmt = udl_stats.update(values={udl_stats.c.last_pdf_task_requested: func.now()}).where(udl_stats.c.state_code == state_code).where(udl_stats.c.tenant == tenant).where(udl_stats.c.batch_guid == batch_guid)
        connector.execute(stmt)


def prepdf_task(settings):
    '''
    Generate pdfs for students that have new assessments

    :param dict settings:  configuration for the application
    '''
    udl_stats_results = prepare_ed_stats()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get(UdlStatsConstants.TENANT)
        state_code = udl_stats_result.get(UdlStatsConstants.STATE_CODE)
        batch_guid = udl_stats_result.get(UdlStatsConstants.BATCH_GUID)
        fact_asmt_outcome_results = prepare_pre_pdf(tenant, state_code, batch_guid)
        triggered_success = trigger_pre_pdf(settings, state_code, tenant, fact_asmt_outcome_results)
        if triggered_success:
            update_ed_stats_for_prepdf(tenant, state_code, batch_guid)


def run_cron_prepdf(settings):
    '''
    Configure and run cron job to regenerate pdfs for students with new assessment data

    :param dict settings: configuration for the application
    '''
    run_cron_job(settings, 'trigger.pdf.', prepdf_task)
