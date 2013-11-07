'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''
import csv
import logging
from edextract.celery import celery
from edextract.celery import MAX_RETRIES, RETRY_DELAY
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.utils import multi_delete

log = logging.getLogger('smarter')


@celery.task(name="tasks.extract.handle_request",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def handle_request(session, query):
    '''
    celery entry point to take request extraction request from service endpoint.
    it checks availiablity of data, then replies to smarter service point.
    if data is available, it executes extraction query.
    it also handles book keeping for tasks.
    :param session: session for caller, for context security checkings
    :param task_queries: queries from caller
    :param params: request extration input parameters
    '''
    current_task_id = handle_request.request.id
    output_uri = '/tmp/extract_' + current_task_id + '.csv'
    celery_extract_result = generate_csv.delay(session, query,
                                               output_uri=output_uri, batch_id=current_task_id)
    return True


@celery.task(name="tasks.extract.generate_csv",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def generate_csv(session, query, output_uri=None, batch_id=None):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param session: cookie for caller, for context security checkings
    :param extract_queries: extraction query to dump data
    :param params: request extraction input parameters
    :param output_uri: output file uri
    :param batch_id: batch_id for tracking
    '''
    log.info('execute tasks.extract.generate_csv for task ' + batch_id)
    if session is None:
        return False
    tenant = session.get_tenant()
    if tenant is None:
        return False
    with EdCoreDBConnection(tenant) as connection:
        results = connection.get_result(query)
        rows = []
        header = []
        # TODO: why is this here?
        for result in results:
            # remove teacher names from results
            results = multi_delete(result, ['teacher_first_name', 'teacher_middle_name', 'teacher_last_name'])
            if len(header) is 0:
                header = list(result.keys())
            rows.append(list(result.values()))
        with open(output_uri, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            csvwriter.writerow(header)
            for row in rows:
                csvwriter.writerow(row)
        csvfile.close()
