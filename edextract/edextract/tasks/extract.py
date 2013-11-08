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
from edcore.utils.utils import multi_delete
from edextract.status.status import update_extract_stats, ExtractStatus
from edextract.status.constants import Constants
from datetime import datetime


log = logging.getLogger('edextract')


@celery.task(name="tasks.extract.generate",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def generate(session, query, request_id, task_id, file_name):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param session: cookie for caller, for context security checkings
    :param query: extraction query to dump data
    :param params: request extraction input parameters
    :param output_uri: output file uri
    :param batch_id: batch_id for tracking
    '''
    start_time = datetime.now()
    output_uri = '/tmp/' + file_name + str(start_time.strftime("%m-%d-%Y_%H-%M-%S")) + '.csv'
    log.info('execute tasks.extract.generate_csv for task ' + task_id)
    update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.EXTRACTING, Constants.EXTRACT_START: start_time, Constants.CELERY_TASK_ID: generate.request.id})
    if session is None:
        return False
    tenant = session.get_tenant()
    if tenant is None:
        return False

    # TODO: add try/catch, update extract status
    with EdCoreDBConnection(tenant) as connection, open(output_uri, 'w') as csvfile:
        results = connection.get_streaming_result(query)  # this result is a generator
        csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        header = []
        # TODO: why is this here?
        for result in results:
            # remove teacher names from results
            result = multi_delete(result, ['teacher_first_name', 'teacher_middle_name', 'teacher_last_name'])
            if len(header) is 0:
                header = list(result.keys())
                csvwriter.writerow(header)
            row = list(result.values())
            csvwriter.writerow(row)
        csvfile.close()
        update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.EXTRACTED, Constants.EXTRACT_END: datetime.now()})
        # TODO: what does the return values do?
        return True
