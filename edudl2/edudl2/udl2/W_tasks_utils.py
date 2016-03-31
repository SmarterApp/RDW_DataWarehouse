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
Created on Apr 28, 2014

@author: dip
'''
from edudl2.udl2.celery import celery


@celery.task(name="udl2.W_task_utils.handle_group_results")
def handle_group_results(msgs):
    '''
    Return the last msg in the group of tasks
    :param list msgs: list of results from group tasks
    '''
    return msgs[len(msgs) - 1] if msgs else {}
