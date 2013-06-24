'''
Created on Jun 23, 2013

@author: tosako
'''
from database.connector import DBConnection
from smarter.database.datasource import get_datasource_name
from sqlalchemy.sql.expression import select, and_, func, true
from smarter.trigger.database.connector import StatsDBConnection
from apscheduler.scheduler import Scheduler
from smarter.trigger.database.udl_stats import get_ed_stats
from batch.pdf.pdf_generator import PDFGenerator
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_absolute_file_path_name


def prepare_pre_pdf(tenant, state_code, last_pdf_generated):
    '''
    prepare which state and district are pre-cached
    '''
    with DBConnection(name=get_datasource_name(tenant)) as connector:
        fact_asmt_outcome = connector.get_table('fact_asmt_outcome')
        query = select([fact_asmt_outcome.c.student_guid.label('student_guid'),
                        fact_asmt_outcome.c.asmt_period_year.label('asmt_period_year'),
                        fact_asmt_outcome.c.district_guid.label('district_guid'),
                        fact_asmt_outcome.c.school_guid.label('school_guid'),
                        fact_asmt_outcome.c.asmt_grade.label('asmt_grade'),
                        ], from_obj=[fact_asmt_outcome])
        query = query.where(fact_asmt_outcome.c.asmt_create_date > last_pdf_generated)
        query = query.where(and_(fact_asmt_outcome.c.state_code == state_code))
        query = query.where(and_(fact_asmt_outcome.c.most_recent == true()))
        results = connector.get_result(query)
        return results


def trigger_pre_pdf(settings, tenant, state_code, results):
    '''
    call pre-pdf function
    '''
    triggered = False
    base_dir = settings.get('pdf.report_base_dir', "/tmp")
    try:
        if len(results) > 0:
            triggered = True
            pdf_trigger = PDFGenerator(settings, tenant)
            for result in results:
                student_guid = result.get('student_guid')
                asmt_period_year = result.get('asmt_period_year')
                district_guid = result.get('district_guid')
                school_guid = result.get('school_guid')
                asmt_grade = result.get('asmt_grade')
                student_guid = result.get('student_guid')
                datasource_name = get_datasource_name(tenant)
                file_name = generate_isr_absolute_file_path_name(pdf_report_base_dir=base_dir, state_code=state_code, asmt_period_year=asmt_period_year, district_guid=district_guid, school_guid=school_guid, asmt_grade=asmt_grade, student_guid=student_guid, datasource=datasource_name)
                pdf_trigger.send_pdf_request(student_guid=student_guid, file_name=file_name)
    except:
        triggered = False
    return triggered


def update_ed_stats_for_prepdf(tenant, state_code):
    '''
    update current timestamp to last_pdf_generated field
    '''
    with StatsDBConnection() as connector:
        udl_stats = connector.get_table('udl_stats')
        stmt = udl_stats.update(values={udl_stats.c.last_pdf_generated: func.now()}).where(udl_stats.c.state_code == state_code).where(udl_stats.c.tenant == tenant)
        connector.execute(stmt)


def prepdf_task(settings):
    udl_stats_results = get_ed_stats()
    for udl_stats_result in udl_stats_results:
        tenant = udl_stats_result.get('tenant')
        state_code = udl_stats_result.get('state_code')
        last_pdf_generated = udl_stats_result.get('last_pdf_generated')
        fact_asmt_outcome_results = prepare_pre_pdf(tenant, state_code, last_pdf_generated)
        triggered_success = trigger_pre_pdf(settings, tenant, fact_asmt_outcome_results)
        if triggered_success:
            update_ed_stats_for_prepdf(tenant, state_code)


def run_cron_recache(settings):
    cron_time = {}
    year = settings.get("trigger.pdf.schedule.cron.year")
    month = settings.get("trigger.pdf.schedule.cron.month")
    day = settings.get("trigger.pdf.schedule.cron.day")
    week = settings.get("trigger.pdf.schedule.cron.week")
    day_of_week = settings.get("trigger.pdf.schedule.cron.day_of_week")
    hour = settings.get("trigger.pdf.schedule.cron.hour")
    minute = settings.get("trigger.pdf.schedule.cron.minute")
    second = settings.get("trigger.pdf.schedule.cron.second")

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
        sched.add_cron_job(prepdf_task, args=[settings], **cron_time)
