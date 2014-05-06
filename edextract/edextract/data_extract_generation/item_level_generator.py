__author__ = 'nestep'

"""
This module contains the logic to write to an assessment item-level CSV extract file.
"""

import os

from edextract.utils.csv_writer import write_csv
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from edextract.status.status import ExtractStatus, insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection
from pyramid.threadlocal import get_current_registry
import logging

logger = logging.getLogger(__name__)


def generate_items_csv(tenant, output_file, task_info, extract_args):
    """
    Write item-level data to CSV file

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_items_csv
    """
    # Get stuff
    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    items_root_dir = get_current_registry().settings.get('extract.item_level_base_dir', '/opt/edware/item_level')

    with EdCoreDBConnection(state_code=extract_args[TaskConstants.STATE_CODE]) as connection:
        # Get results (streamed, it is important to avoid memory exhaustion)
        results = connection.get_streaming_result(query)

        # Write the header to the file
        # TODO: Should not be hard coded
        if not os.path.exists(output_file):
            write_csv(output_file,
                      ['position', 'segmentId', 'key', 'clientId', 'operational', 'isSelected', 'format', 'score',
                       'scoreStatus', 'adminDate', 'numberVisits', 'strand', 'contentLevel', 'pageNumber', 'pageVisits',
                       'pageTime', 'dropped'],
                      [])

        # Open the file to stream it out
        with open(output_file, 'a') as out_file:
            # Read each result for item-level data
            for result in results:
                # Build path to file
                path = _get_path_to_item_csv(items_root_dir, result)

                # If the file exists, stream the file into the output file
                if os.path.exists(path):
                    with open(path, 'r') as in_file:
                        out_file.write(in_file.read())

        # Done
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _get_path_to_item_csv(items_root_dir, record):
    return os.path.join(items_root_dir, str(record['code_state']).upper(), str(record['asmt_year']),
                        str(record['asmt_type']).upper().replace(' ', '_'), str(record['effective_date']),
                        str(record['asmt_subject']).upper(), str(record['grade_asmt']), str(record['guid_district']),
                        (str(record['guid_student']) + '.csv'))
