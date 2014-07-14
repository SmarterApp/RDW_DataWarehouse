__author__ = 'sravi'

"""
This module contains the logic to gather raw xml files to output directory for archiving
"""

import logging
import os
import shutil
from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.status.constants import Constants
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.tasks.constants import Constants as TaskConstants, QueryType

logger = logging.getLogger(__name__)


def generate_raw_data_xml(tenant, output_paths, task_info, extract_args):
    """
    Write raw xml data to output file

    @param tenant: Requestor's tenant ID
    @param output_paths: list of output path name's to place the selected raw data xml files
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_raw_data_xml
    """
    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    root_dir = extract_args[TaskConstants.ROOT_DIRECTORY]
    if type(output_paths) is not list:
        output_paths = [output_paths]

    with EdCoreDBConnection(tenant=tenant) as connection:
        # Get results (streamed, it is important to avoid memory exhaustion)
        results = connection.get_streaming_result(query)
        for result in results:
            # Build path to file
            source_file = _get_path_to_raw_xml(root_dir, result)

            # Test hack for now to place all raw data xml files in  first folder
            # this line needs to be removed and replaced with call to get what input files
            # will go in to what output folders based on zipping threshold
            output_path = output_paths[0]
            # end of hack lines

            # copy the above source raw xml file to output directory to be archived
            _copy_file_out(source_file, output_path)

        # Done
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _get_path_to_raw_xml(root_dir, record):
    return os.path.join(root_dir, str(record['state_code']).upper(), str(record['asmt_year']),
                        str(record['asmt_type']).upper().replace(' ', '_'), str(record['effective_date']),
                        str(record['asmt_subject']).upper(), str(record['asmt_grade']), str(record['district_guid']),
                        (str(record['student_guid']) + '.xml'))


def _copy_file_out(source, destination):
    if os.path.exists(source):
        shutil.copy2(source, destination)
