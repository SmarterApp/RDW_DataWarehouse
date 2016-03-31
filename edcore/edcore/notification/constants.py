# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Sep 4, 2014

@author: tosako
'''


class Constants():
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'
    # notification
    STUDENT_REG_GUID = 'student_reg_guid'
    REG_SYSTEM_ID = 'reg_system_id'
    CALLBACK_URL = 'callback_url'
    EMAILNOTIFICATION = 'email_notification'
    ATTEMPT_NUMBER = 'attempt_number'
    NOTIFICATION_ERRORS = 'notification_errors'
    ACADEMIC_YEAR = 'academic_year'
    TOTAL_ROWS_LOADED = 'total_rows_loaded'
    TOTAL_ROWS_NOT_LOADED = 'total_rows_not_loaded'
    GUID_BATCH = 'guid_batch'
    UDL2_BATCH_TABLE = 'udl_batch'
    BATCH_TABLE = 'batch_table'
    NOTIFICATION_MAX_ATTEMPTS = 'notification_max_attempts'
    NOTIFICATION_RETRY_INTERVAL = 'notification_retry_interval'
    NOTIFICATION_TIMEOUT_INTERVAL = 'notification_timeout_interval'
    UDL_PHASE = 'udl_phase'
    UDL_PHASE_STEP_STATUS = 'udl_phase_step_status'
    ERROR_DESC = 'error_desc'
    MAIL_SERVER = 'migrate.notification.mail_server'
    MAIL_SENDER = 'migrate.notification.mail_sender'
