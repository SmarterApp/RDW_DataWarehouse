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
Created on Mar 21, 2014

@author: tosako
'''
from kombu.entity import Exchange, Queue
from edmigrate.utils.constants import Constants


exchange = Exchange(Constants.CONDUCTOR_EXCHANGE, type='direct')
queue = Queue(Constants.CONDUCTOR_QUEUE, exchange=exchange, routing_key=Constants.CONDUCTOR_ROUTING_KEY, durable=False)
