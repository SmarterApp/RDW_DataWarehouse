__author__ = 'nestep'

"""
This module contains the logic to write to an assessment item-level CSV extract file.
"""

import csv
import logging
import os

from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.status.constants import Constants
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from edextract.utils.csv_writer import write_csv

logger = logging.getLogger(__name__)

ITEM_KEY_POS = 0


def generate_items_csv(tenant, output_files, task_info, extract_args):
    """
    Write item-level data to CSV file

    @param tenant: Requestor's tenant ID
    @param output_files: List of output file path's for item extract
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_items_csv
    """
    # Get stuff
    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    items_root_dir = extract_args[TaskConstants.ROOT_DIRECTORY]
    item_ids = extract_args[TaskConstants.ITEM_IDS]
    checking_ids = item_ids is not None

    with EdCoreDBConnection(tenant=tenant) as connection:
        # Get results (streamed, it is important to avoid memory exhaustion)
        results = connection.get_streaming_result(query)

        # Write the header to the file
        # TODO: Should not be hard coded
        for output_file in output_files:
            if not os.path.exists(output_file):
                write_csv(output_file,
                          ['key', 'student_guid', 'segmentId', 'position', 'clientId', 'operational', 'isSelected',
                           'format', 'score', 'scoreStatus', 'adminDate', 'numberVisits', 'strand', 'contentLevel',
                           'pageNumber', 'pageVisits', 'pageTime', 'dropped'],
                          [])

        # Test hack for now to write all content to first file, other files will have only headers
        # this line needs to be removed and replaced with call to get what input files
        # will go in to what output files based on output file threshold
        output_file = output_files[0]
        # end of hack lines

        # Open the file to stream it out
        with open(output_file, 'a') as out_file:
            # Read each result for item-level data
            for result in results:
                # Build path to file
                path = _get_path_to_item_csv(items_root_dir, result)

                # Write this file to output file if we are not checking for specific item IDs or if this file contains
                # at least one of the requested item IDs
                if not checking_ids or _check_file_for_items(path, item_ids):
                    _write_file_out(path, out_file)

        # Done
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _get_path_to_item_csv(items_root_dir, record):
    return os.path.join(items_root_dir, str(record['state_code']).upper(), str(record['asmt_year']),
                        str(record['asmt_type']).upper().replace(' ', '_'), str(record['effective_date']),
                        str(record['asmt_subject']).upper(), str(record['asmt_grade']), str(record['district_guid']),
                        (str(record['student_guid']) + '.csv'))


def _check_file_for_items(path, item_ids):
    if os.path.exists(path):
        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if row[ITEM_KEY_POS] in item_ids:
                    return True
    return False


def _write_file_out(path, out_file):
    if os.path.exists(path):
        with open(path, 'r') as in_file:
            out_file.write(in_file.read())
