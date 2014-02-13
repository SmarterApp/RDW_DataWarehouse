import logging
import os
import shutil

__author__ = 'sravi'

logger = logging.getLogger(__name__)


def cleanup_work_zone(work_zone_directories_to_cleanup):

    """
    Remove all the directories in the given dict
    :param work_zone_directories_to_cleanup: a dictionary of directories
    :return:
    """
    for directory in work_zone_directories_to_cleanup.values():
        # cleanup the entire directory recursively
        if os.path.exists(directory):
            shutil.rmtree(directory)
    return True
