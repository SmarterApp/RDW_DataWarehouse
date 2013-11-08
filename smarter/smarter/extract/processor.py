'''
Celery Tasks for data extraction

Created on Nov 5, 2013

@author: ejen
'''
import logging
from smarter.reports.helpers.constants import Constants
from smarter.extract.constants import Constants as Extract
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.extract.student_assessment import get_extract_assessment_query
from pyramid.security import authenticated_userid
from uuid import uuid4
from edextract.status.status import create_new_status, ExtractStatus
from edextract.tasks.extract import generate
import edextract
from pyramid.threadlocal import get_current_request


log = logging.getLogger('smarter')


def process_extraction_request(params):
    '''
    :param dict params: contains query parameter.  Value for each pair is expected to be a list
    '''
    tasks = []
    for e in params[Extract.EXTRACTTYPE]:
        for s in params[Constants.ASMTSUBJECT]:
            for t in params[Constants.ASMTTYPE]:
                # TODO: handle year and stateCode/tenant
                tasks.append({Extract.EXTRACTTYPE: e,
                              Constants.ASMTSUBJECT: s,
                              Constants.ASMTTYPE: t,
                              Constants.ASMTYEAR: params[Constants.ASMTYEAR][0],
                              Constants.STATECODE: params[Constants.STATECODE][0]})
    task_responses = []
    # Generate an uuid for this extract request
    request_id = str(uuid4())

    for task in tasks:
        response = {Constants.STATECODE: task[Constants.STATECODE],
                    Extract.EXTRACTTYPE: task[Extract.EXTRACTTYPE],
                    Constants.ASMTSUBJECT: task[Constants.ASMTSUBJECT],
                    Constants.ASMTTYPE: task[Constants.ASMTTYPE],
                    #Constants.ASMTYEAR: task[Constants.ASMTYEAR],
                    Extract.REQUESTID: request_id}
        extract_query = get_extract_assessment_query(task, compiled=True)
        check_query = get_extract_assessment_query(task, limit=1)

        if has_data(check_query, request_id):
            user = authenticated_userid(get_current_request())
            tenant = user.get_tenant()
            task_id = create_new_status(user, request_id, task, ExtractStatus.QUEUED)
            file_name = __get_file_name(task)
            # Call async celery task.  Kwargs set up queue name in prod mode
            celery_response = generate.delay(tenant, extract_query, request_id, task_id, file_name, **edextract.celery.KWARGS)  # @UndefinedVariable
            task_id = celery_response.task_id
            response[Extract.STATUS] = Extract.OK
            response[Constants.ID] = task_id
        else:
            response[Extract.STATUS] = Extract.FAIL
            response[Extract.MESSAGE] = "Data is not available"
        task_responses.append(response)
    return task_responses


def has_data(query, request_id):
    log.info('Extract: data availability check for request ' + request_id)
    with EdCoreDBConnection() as connection:
        result = connection.get_result(query.limit(1))
    if result is None or len(result) < 1:
        return False
    else:
        return True


def __get_file_name(param):
    return 'ASMT_' + param[Constants.STATECODE] + '_' + param[Constants.ASMTSUBJECT] + '_' + param[Constants.ASMTTYPE] + "_"
