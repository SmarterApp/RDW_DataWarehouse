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
Created on Mar 27, 2014

@author: tosako
'''
import logging


class MockLogger(logging.Logger):

    def __init__(self, *args, **kwargs):
        self.logged = []
        logging.Logger.__init__(self, *args, **kwargs)

    def _log(self, level, msg, args, **kwargs):
        self.logged.append((level, msg, args, kwargs))
