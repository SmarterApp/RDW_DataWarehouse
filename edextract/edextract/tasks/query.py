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
from edextract.celery import TIMEOUT
import services
from celery.exceptions import MaxRetriesExceededError
from edcore.database.stats_connector import StatsDBConnection
from edextract.status.status import insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection

OK = 0
FAIL = 1

log = logging.getLogger('smarter')


@celery.task(name="tasks.extract.handle_request",
             max_retries=services.celery.MAX_RETRIES,
             default_retry_delay=services.celery.RETRY_DELAY)
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
    celery_check_result = is_available.delay(cookie=cookie, check_query=task_queries[0])
    print(celery_check_result)
    if celery_check_result.get():
        print('data exists')
        output_uri = '/tmp/extract_' + current_task_id + '.csv'
        celery_extract_result = generate_csv.delay(cookie=cookie, extract_query=task_queries[1], output_uri=output_uri)
        return True
    else:
        return False


@celery.task(name="tasks.extract.is_available",
             max_retries=services.celery.MAX_RETRIES,
             default_retry_delay=services.celery.RETRY_DELAY)
def is_available(cookie=None, check_query=None):
    '''
    celery entry point to execute data availability check query.
    it checks availiablity of data, then replies to smarter service point.
    :param cookie: cookie for caller, for context security checkings
    :param check_queries: data availablitly query
    '''
    with EdCoreDBConnection() as connection:
        result = connection.execute(check_query).fetchone()
        #result.close()
    if len(result) >= 1:
        return True
    else:
        return False


@celery.task(name="tasks.extract.generate_csv",
             max_retries=services.celery.MAX_RETRIES,
             default_retry_delay=services.celery.RETRY_DELAY)
def generate_csv(cookie=None, extract_query=None, output_uri=None):
    '''
    celery entry point to execute data extraction query.
    it execute extraction query and dump data into csv file that specified in output_uri
    :param cookie: cookie for caller, for context security checkings
    :param extract_queries: extraction query to dump data
    :param output_uri: output file uri
    '''
    print('execute tasks.extract.generate_csv')

    with EdCoreDBConnection() as connection:
        counter = 0
        result = connection.execute(extract_query)
        rows = result.fetchall()
        with open(output_uri, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                csvwriter.writerow(row)
        csvfile.close()
        result.close()
