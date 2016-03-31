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

#!/bin/env python
import argparse
import subprocess

from pyinotify import WatchManager, Notifier, ProcessEvent, IN_MOVED_TO

__author__ = 'swimberly'


class EventHandler(ProcessEvent):

    def process_IN_MOVED_TO(self, event):
        if not event.dir:
            print("file created and written:", event.pathname)
            cmd = 'driver.py -a {}'.format(event.pathname)
            subprocess.call(cmd, shell=True)


def monitor_directory(directory_path):
    """
    Loop indefinately while the directory path is monitored
    When a new file is added kick off the pipeline
    :param directory_path: The path to the directory
    :return: Never
    """
    wm = WatchManager()

    # sftp/scp modules usually create temporary files during transfer and move them to permanent
    # file after entire transfer is complete. This way we only need to watch for IN_MOVE_TO events
    mask = IN_MOVED_TO  # watched events

    handler = EventHandler()
    notifier = Notifier(wm, handler)
    _wdd = wm.add_watch(directory_path, mask, rec=True, auto_add=True)

    notifier.loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to kick off the pipeline whenever a new file is added')
    parser.add_argument('-d', '--directory', required=True, help='The path to the directory to monitor')
    args = parser.parse_args()

    monitor_directory(args.directory)
