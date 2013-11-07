'''
Celery Tasks for data extraction

Created on Nov 5, 2013

@author: ejen
'''
import logging
from smarter.reports.helpers.constants import Constants
from edextract.tasks.query import handle_request
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.extract.smarter_extraction import get_extract_assessment_query


log = logging.getLogger('smarter')


def process_extraction_request(session, params):
    '''
    :param session:
    :param params:
    '''
    tasks = []
    for e in params['extractType']:
        for s in params[Constants.ASMTSUBJECT]:
            for t in params[Constants.ASMTTYPE]:
                #  We'll need to reimplement for year and stateCode, or just add a for loop
                # TODO: define constants
                # TODO: copy constnats from smarter to edextract
                tasks.append({'extractType': e, Constants.ASMTSUBJECT: s, Constants.ASMTTYPE: t, Constants.ASMTYEAR: params[Constants.ASMTYEAR][0], Constants.STATECODE: params[Constants.STATECODE][0]})
    task_responses = []

    # TODO: Generate an id, to identify the batch_id here

    for task in tasks:
        # TODO: use constants
        response = {Constants.ASMTYEAR: task[Constants.ASMTYEAR],
                    Constants.STATECODE: task[Constants.STATECODE],
                    'extractType': task["extractType"],
                    Constants.ASMTSUBJECT: task[Constants.ASMTSUBJECT],
                    Constants.ASMTTYPE: task[Constants.ASMTTYPE]}
        query = get_extract_assessment_query(task)
        if has_data(session, query):
            celery_response = handle_request.delay(session, query)    # @UndefinedVariable
            task_id = celery_response.task_id
            response['status'] = Constants.OK
            response[Constants.ID] = task_id
        else:
            response['status'] = Constants.FAIL
            response['message'] = "Data is not available"
        task_responses.append(response)
    return task_responses


# TODO:  do we need batch id here?
def has_data(session, query, batch_id="TODO"):
    log.info('extract check query for task ' + batch_id)
    if session is None:
        return False
    tenant = session.get_tenant()
    if tenant is None:
        return False
    with EdCoreDBConnection(tenant) as connection:
        result = connection.get_result(query.limit(1))
    if result is None or len(result) < 1:
        return False
    else:
        return True
