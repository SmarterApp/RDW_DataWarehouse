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

import time


class WaitExpiredException(Exception):
    pass


def wait_function(function, seconds_to_wait=5):
    timer = 0
    while timer <= seconds_to_wait:
        try:
            return function()
        except Exception:
            timer += 1
            time.sleep(timer)
    raise WaitExpiredException(
        '{t} second[s] expires for "{f}" function'.format(t=seconds_to_wait, f=function.__name__))
