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

