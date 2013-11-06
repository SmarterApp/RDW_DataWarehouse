'''
Celery Tasks for data extraction

Created on Nov 5, 2013

@author: ejen
'''
import os
import sys
import csv
import logging
import subprocess
import platform
from edextract.celery import celery
from edextract.exceptions import ExtractionError
import copy
from edextract.celery import TIMEOUT, MAX_RETRIES, RETRY_DELAY
import services
from celery.exceptions import MaxRetriesExceededError
from edcore.database.stats_connector import StatsDBConnection
from edextract.status.status import insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection

OK = 0
FAIL = 1

log = logging.getLogger('smarter')


@celery.task(name="tasks.extract.handle_request",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def handle_request(cookie=None, task_queries=None):
    '''
    celery entry point to take request extraction request from service endpoint.
    it checks availiablity of data, then replies to smarter service point.
    if data is available, it executes extraction query.
    it also handles book keeping for tasks.
    :param cookie: cookie for caller, for context security checkings
    :param task_queries: queries from caller
    '''
    current_task_id = handle_request.request.id
    celery_check_result = is_available.delay(cookie=cookie, check_query=task_queries[0], batch_id=current_task_id)
    log.info('extract request with id ' + current_task_id)
    if celery_check_result.get():
        output_uri = '/tmp/extract_' + current_task_id + '.csv'
        celery_extract_result = generate_csv.delay(cookie=cookie, extract_query=task_queries[1], output_uri=output_uri, batch_id=current_task_id)
        return True
    else:
        return False


@celery.task(name="tasks.extract.is_available",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def is_available(cookie=None, check_query=None, batch_id=None):
    '''
    celery entry point to execute data availability check query.
    it checks availiablity of data, then replies to smarter service point.
    :param cookie: cookie for caller, for context security checkings
    :param check_queries: data availablitly query
    :param batch_id: the batch_id for tracking
    '''
    log.info('extract check query for task ' + batch_id)
    with EdCoreDBConnection() as connection:
        result = connection.execute(check_query).fetchone()
    if result is None or len(result) < 1:
        return False
    else:
        return True


@celery.task(name="tasks.extract.generate_csv",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def generate_csv(cookie=None, extract_query=None, output_uri=None, batch_id=None):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param cookie: cookie for caller, for context security checkings
    :param extract_queries: extraction query to dump data
    :param output_uri: output file uri
    :param batch_id: batch_id for tracking
    '''
    log.info('execute tasks.extract.generate_csv for task ' + batch_id)
    with EdCoreDBConnection() as connection:
        counter = 0
        result = connection.execute(extract_query)
        if result is not None:
            rows = result.fetchall()
        else:
            rows = []
        with open(output_uri, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                csvwriter.writerow(row)
        csvfile.close()
