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

import os
import time


class FileUtilsException(Exception):
    pass


def find_file(path, extension='.zip', timeout=20):
    end_time = time.time() + timeout

    while end_time >= time.time():
        for next_file in os.listdir(path):
            if next_file.endswith(extension):
                if path.endswith('/'):
                    return path + next_file
                else:
                    return path + '/' + next_file
        time.sleep(0.5)
    raise FileUtilsException(
        "Unable to find file with '{e}' extension by the following path: {path}".format(e=extension, path=path))
