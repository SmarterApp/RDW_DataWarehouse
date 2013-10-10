import argparse
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

__author__ = 'swimberly'


class EventHandler(ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        print("file created and written:", event.pathname)


def monitor_directory(directory_path):
    """
    Loop indefinately while the directory path is monitored
    When a new file is added kick off the pipeline
    :param directory_path: The path to the directory
    :return: Never
    """
    wm = WatchManager()

    mask = EventsCodes.IN_CLOSE_WRITE  # watched events

    handler = EventHandler()
    notifier = Notifier(wm, handler)
    _wdd = wm.add_watch(directory_path, mask, rec=True)

    notifier.loop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to kick off the pipeline whenever a new file is added')
    parser.add_argument('-d', '--directory', required=True, help='The path to the directory to monitor')
    args = parser.parse_args()

    monitor_directory(args.directory)

