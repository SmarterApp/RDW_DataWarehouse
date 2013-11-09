'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''
import csv
import logging
from edextract.celery import celery
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.utils.utils import multi_delete
from edextract.status.status import update_extract_stats, ExtractStatus
from edextract.status.constants import Constants
from edextract.utils.file_encryptor import FileEncryptor
from datetime import datetime
from edextract.settings.config import Config, get_setting


log = logging.getLogger('edextract')


@celery.task(name="tasks.extract.generate",
             max_retries=get_setting(Config.MAX_RETRIES),
             default_retry_delay=get_setting(Config.RETRY_DELAY))
def generate(tenant, user_name, query, request_id, task_id, file_name):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param tenant: tenant of the user
    :param user_name: user_id of the user
    :param query: extraction query to dump data
    :param params: request extraction input parameters
    :param output_uri: output file uri
    :param batch_id: batch_id for tracking
    '''
    start_time = datetime.now()
    output_uri = '/tmp/' + file_name + str(start_time.strftime("%m-%d-%Y_%H-%M-%S")) + '.csv.gz.pgp'
    log.info('execute tasks.extract.generate_csv for task ' + task_id)
    try:
        update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.EXTRACTING, Constants.EXTRACT_START: start_time, Constants.CELERY_TASK_ID: generate.request.id})
        if tenant is None:
            update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.NO_TENANT, Constants.EXTRACT_END: datetime.now()})
            return False
        # TODO: Better way to manage file name extension and retrieve public from specific user.
        with EdCoreDBConnection(tenant) as connection, FileEncryptor(output_file=output_uri, recipient='Example User') as csvfile:
            results = connection.get_streaming_result(query)  # this result is a generator
            csvwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            header = []
            for result in results:
                # remove teacher names from results
                result = multi_delete(result, ['teacher_first_name', 'teacher_middle_name', 'teacher_last_name'])
                if len(header) is 0:
                    header = list(result.keys())
                    csvwriter.writerow(header)
                row = list(result.values())
                csvwriter.writerow(row)
            csvfile.close()
            update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.EXTRACTED,
                                           Constants.EXTRACT_END: datetime.now(),
                                           Constants.OUTPUT_FILE: output_uri})
            # TODO: what does the return values do?
            return True
    except Exception as e:
        log.error(e)
        update_extract_stats(task_id, {Constants.EXTRACT_STATUS: ExtractStatus.FAILED, Constants.EXTRACT_END: datetime.now()})
        return False
