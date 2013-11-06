'''
Celery Tasks for data extraction for

Created on Nov 5, 2013

@author: ejen
'''
import os
import sys
import csv
import logging
from edextract.celery import celery
from edextract.exceptions import ExtractionError
from edextract.celery import TIMEOUT, MAX_RETRIES, RETRY_DELAY
from celery.exceptions import MaxRetriesExceededError
from edcore.database.stats_connector import StatsDBConnection
from edextract.status.status import insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.extracts.smarter_extraction import FUNCTION_MAP
from pyramid.security import authenticated_userid
from smarter.reports.helpers.utils import multi_delete

OK = 0
FAIL = 1

log = logging.getLogger('smarter')

@celery.task(name="tasks.extract.handle_request",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def handle_request(session=None, task_queries=None, params=None):
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
    celery_check_result = is_available.delay(session=session, check_query=task_queries[0], params=params,
                                             batch_id=current_task_id)
    log.info('extract request with id ' + current_task_id)
    if celery_check_result.get():
        output_uri = '/tmp/extract_' + current_task_id + '.csv'
        celery_extract_result = generate_csv.delay(session=session, extract_query=task_queries[1], params=params,
                                                   output_uri=output_uri, batch_id=current_task_id)
        return True
    else:
        return False


@celery.task(name="tasks.extract.is_available",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def is_available(session=None, check_query=None, params=None, batch_id=None):
    '''
    celery entry point to execute data availability check query.
    it checks availiablity of data, then replies to smarter service point.
    :param session: session for caller, for context security checkings
    :param check_queries: data availablitly query
    :param params: request extraction input parameters
    :param batch_id: the batch_id for tracking
    '''
    log.info('extract check query for task ' + batch_id)
    if session is None:
        return False
    tenant = session.get_tenant()
    if tenant is None:
        return False
    with EdCoreDBConnection(tenant) as connection:
        result = connection.get_result(FUNCTION_MAP[check_query](params))
    if result is None or len(result) < 1:
        return False
    else:
        return True


@celery.task(name="tasks.extract.generate_csv",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def generate_csv(session=None, extract_query=None, params=None, output_uri=None, batch_id=None):
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
        counter = 0
        results = connection.get_result(FUNCTION_MAP[extract_query](params))
        rows = []
        header = []
        for result in results:
            # remove teacher names from results
            results = multi_delete(result, ['teacher_first_name', 'teacher_middle_name', 'teacher_last_name'])
            if len(header) is 0:
                header = list(result.keys())
            rows.append(list(result.values()))
        with open(output_uri, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(header)
            for row in rows:
                csvwriter.writerow(row)
        csvfile.close()
