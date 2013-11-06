'''
Celery Tasks for data extraction

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
from smarter.reports.helpers.constants import Constants
from edextract.extracts.smarter_extraction import QUERY_MAP
from edextract.tasks.query import handle_request


log = logging.getLogger('smarter')


@celery.task(name="tasks.send_extraction_request",
             max_retries=MAX_RETRIES,
             default_retry_delay=RETRY_DELAY)
def process_extraction_request(session, params):
    '''
    :param session:
    :param params:
    '''
    query_lookups = []
    for e in params['extractType']:
        for s in params['asmtSubject']:
            for t in params['asmtType']:
                query_lookups.append(e + '_' + s + '_' + t)
    tasks = []
    task_responses = []

    for l in query_lookups:
        query_calls = QUERY_MAP[l]
        queries = []
        for q in query_calls:
            queries.append(q)
        tasks.append({'key': l, 'queries': queries, 'params': params})


    for task in tasks:
        celery_response = handle_request.delay(session=session, task_queries=task['queries'], params=params)
        task_id = celery_response.task_id
        key_parts = task['key'].split('_')
        status = celery_response.get()
        if status:
            task_responses.append({
                'status': Constants.OK,
                'id': task_id,
                'asmtYear': params['asmtYear'][0],
                'stateCode': params['stateCode'][0],
                'extractractType': key_parts[0],
                'asmtSubject': key_parts[1],
                'asmtType': key_parts[2]
            })
        else:
            task_responses.append({
                'status': Constants.FAIL,
                'message': 'Data is not available',
                'id': task_id,
                'asmtYear': params['asmtYear'][0],
                'stateCode': params['stateCode'][0],
                'extractractType': key_parts[0],
                'asmtSubject': key_parts[1],
                'asmtType': key_parts[2]
            })
    return task_responses