'''
Created on Sep 4, 2014

@author: tosako
'''
import logging
import json
from requests import post
import requests.exceptions as req_exc
from edcore.notification.Constants import Constants


logger = logging.getLogger('edcore')


def post_notification(callback_url, timeout_interval, notification_body):
    """
    Send an HTTP POST request with the job status and any errors, and wait for a reply.
    If HTTP return status is "SUCCESS", return with SUCCESS status.
    If HTTP return status is contained within certain predetermined codes, attempt to retry.
    If HTTP return status is other than the retry codes, or wait timeout is reached,
    return with FAILURE status and the reason.

    @param callback_url: Callback URL to which to post the notification
    @param timeout_interval: HTTP POST timeout setting
    @param notification_body: Body of notification HTTP POST request

    @return: Notification status and messages
    """

    retry_codes = [408]

    # Attempt HTTP POST of notification body.
    status_code = 0

    logger.debug('Notification payload -- %s' % json.dumps(notification_body))

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    try:
        response = post(callback_url, json.dumps(notification_body), timeout=timeout_interval, headers=headers)
        status_code = response.status_code

        # Throw an exception for all responses but success.
        response.raise_for_status()

        # Success!
        notification_status = Constants.SUCCESS
        notification_error = None

    except (req_exc.ConnectionError, req_exc.Timeout) as exc:
        # Retryable error.
        notification_status = Constants.PENDING
        notification_error = str(exc.args[0])

    except (req_exc.HTTPError) as exc:
        # Possible retryable error.  Retry if status code indicates so.
        notification_error = str(exc.args[0])
        if status_code in retry_codes:
            notification_status = Constants.PENDING
        else:
            notification_status = Constants.FAILURE

    except req_exc.RequestException as exc:
        # Non-retryable requests-related exception; don't retry.
        notification_status = Constants.FAILURE
        notification_error = str(exc.args[0])

    except Exception as exc:
        # Non-requests-related exception; don't retry.
        notification_status = Constants.FAILURE
        notification_error = str(exc.args[0])

    return notification_status, notification_error
