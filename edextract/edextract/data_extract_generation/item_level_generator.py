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
from edextract.utils.file_utils import File
import copy

logger = logging.getLogger(__name__)

ITEM_KEY_POS = 0
# Write the header to the file
# TODO: Should not be hard coded
CSV_HEADER = ['key', 'student_guid', 'segmentId', 'position', 'clientId', 'operational', 'isSelected',
              'format', 'score', 'scoreStatus', 'adminDate', 'numberVisits', 'strand', 'contentLevel',
              'pageNumber', 'pageVisits', 'pageTime', 'dropped']

def generate_items_csv(tenant, output_files, task_info, extract_args):
    '''
    Write item-level data to CSV file

    @param tenant: Requestor's tenant ID
    @param output_files: List of output file path's for item extract
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_items_csv
    '''
    # Get stuff
    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    items_root_dir = extract_args[TaskConstants.ROOT_DIRECTORY]
    item_ids = extract_args[TaskConstants.ITEM_IDS]

    with EdCoreDBConnection(tenant=tenant) as connection:
        # Get results (streamed, it is important to avoid memory exhaustion)
        results = connection.get_streaming_result(query)

        _append_csv_files(items_root_dir, item_ids, results, output_files, CSV_HEADER)
        # Done
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _get_path_to_item_csv(items_root_dir, state_code=None, asmt_year=None, asmt_type=None, effective_date=None, asmt_subject=None, asmt_grade=None, district_guid=None, student_guid=None):
    if type(asmt_year) is int:
        asmt_year = str(asmt_year)
    path = items_root_dir
    if state_code is not None:
        path = os.path.join(path, state_code)
    else:
        return path
    if asmt_year is not None:
        path = os.path.join(path, asmt_year)
    else:
        return path
    if asmt_type is not None:
        path = os.path.join(path, asmt_type.upper().replace(' ', '_'))
    else:
        return path
    if effective_date is not None:
        path = os.path.join(path, effective_date)

    if asmt_subject is not None:
        path = os.path.join(path, asmt_subject.upper())
    else:
        return path
    if asmt_grade is not None:
        path = os.path.join(path, asmt_grade)
    else:
        return path
    if district_guid is not None:
        path = os.path.join(path, district_guid)
    else:
        return path
    if student_guid is not None:
        path = os.path.join(path, student_guid + '.csv')
    return path


def _check_file_for_items(file_descriptor, item_ids):
    csv_reader = csv.reader(file_descriptor, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for row in csv_reader:
        if row[ITEM_KEY_POS] in item_ids:
            return True
    return False


def _append_csv_files(items_root_dir, item_ids, results, output_files, csv_header):

    def open_outfile(output_file):
        _file = open(output_file, 'w')
        csvwriter = csv.writer(_file, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_header)
        return _file

    _output_files = copy.deepcopy(output_files)
    files = _prepare_file_list(items_root_dir, results)
    number_of_files = len(_output_files)
    threshold_size = -1
    if number_of_files > 1:
        total_file_size = sum(file.size for file in files)
        threshold_size = int(total_file_size / len(_output_files))

    out_file = None
    for file in files:
        # Write this file to output file if we are not checking for specific item IDs or if this file contains
        # at least one of the requested item IDs
        with open(file.name, 'r') as in_file:
            if item_ids is None or _check_file_for_items(in_file, item_ids):
                in_file.seek(0)
                if out_file is not None and threshold_size > 0 and out_file.tell() + file.size > threshold_size and _output_files:
                    # close current out_file
                    out_file.close()
                    out_file = None
                if out_file is None:
                    output_file = _output_files.pop(0)
                    out_file = open_outfile(output_file)
                out_file.write(in_file.read())

    if out_file is not None:
        out_file.close()


def _prepare_file_list(items_root_dir, results):
    files = []
    for result in results:
        path = _get_path_to_item_csv(items_root_dir, **result)
        file = File(path)
        files.append(file)
    return files
