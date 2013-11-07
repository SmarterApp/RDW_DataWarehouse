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
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from uuid import uuid4


log = logging.getLogger('smarter')


def process_extraction_request(params):
    '''
    :param params:
    '''
    tasks = []
    for e in params[Constants.EXTRACTTYPE]:
        for s in params[Constants.ASMTSUBJECT]:
            for t in params[Constants.ASMTTYPE]:
                # TODO: handle year and stateCode/tenant
                tasks.append({Constants.EXTRACTTYPE: e,
                              Constants.ASMTSUBJECT: s,
                              Constants.ASMTTYPE: t,
                              Constants.ASMTYEAR: params[Constants.ASMTYEAR][0],
                              Constants.STATECODE: params[Constants.STATECODE][0]})
    task_responses = []
    request_id = str(uuid4())

    for task in tasks:
        response = {Constants.ASMTYEAR: task[Constants.ASMTYEAR],
                    Constants.STATECODE: task[Constants.STATECODE],
                    Constants.EXTRACTTYPE: task[Constants.EXTRACTTYPE],
                    Constants.ASMTSUBJECT: task[Constants.ASMTSUBJECT],
                    Constants.ASMTTYPE: task[Constants.ASMTTYPE],
                    Constants.REQUESTID: request_id}
        extract_query = get_extract_assessment_query(task, compiled=True)
        check_query = get_extract_assessment_query(task, limit=1)

        if has_data(check_query, request_id):
            user = authenticated_userid(get_current_request())
            # Call async celery task
            celery_response = handle_request.delay(user, extract_query, request_id)    # @UndefinedVariable
            response[Constants.STATUS] = Constants.OK
            response[Constants.ID] = celery_response.task_id
        else:
            response[Constants.STATUS] = Constants.FAIL
            response[Constants.MESSAGE] = "Data is not available"
        task_responses.append(response)
    return task_responses


def has_data(query, request_id):
    log.info('extract check query for extract request ' + request_id)
    with EdCoreDBConnection() as connection:
        result = connection.get_result(query.limit(1))
    if result is None or len(result) < 1:
        return False
    else:
        return True
