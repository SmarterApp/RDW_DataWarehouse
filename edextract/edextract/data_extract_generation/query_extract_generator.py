__author__ = 'tshewchuk'

"""
This module contains the logic to write to an Assessment CSV or JSON extract file.
"""

from itertools import chain
import json

from edextract.utils.json_formatter import format_json
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from edextract.status.status import ExtractStatus, insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.utils.csv_writer import write_csv
import logging

logger = logging.getLogger(__name__)


def generate_csv(tenant, output_file, task_info, extract_args):
    """
    Write data extract to CSV file.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_csv
    """

    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    with EdCoreDBConnection(tenant=tenant) as connection:
        results = connection.get_streaming_result(query)  # this result is a generator
        header, data = _generate_csv_data(results)
        with open(output_file, 'w') as f:
            write_csv(f, data, header=header)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def generate_json(tenant, output_file, task_info, extract_args):
    """
    Write data extract to JSON file.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_json
    """

    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]

    with EdCoreDBConnection(tenant=tenant) as connection, open(output_file, 'w') as json_file:
        results = connection.get_result(query)

        # There should only be one result in the list
        if len(results) is 1:
            formatted = format_json(results[0])
            json.dump(formatted, json_file, indent=4)
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.GENERATED_JSON})
        else:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: "Results length is: " + str(len(results))})


def _generate_csv_data(results):
    """
    Generate the CSV data for the extract.

    @param tenant: ID of tenant for which toe extract data
    @param query: DB query used to extract the data.

    @return: CSV extract header and data
    """
    header = []
    data = []

    try:
        first = next(results)
    except StopIteration as ex:
        logger.error(str(ex))
        return header, data

    header = list(first.keys())
    data = _gen_to_val_list(chain([first], results))

    return header, data


def _gen_to_val_list(dict_gen):
    """
    Convert a generator of dicts into a generator of lists of values for each dict.

    @param dict_gen: Generator of dicts

    @return: Generator of corresponding value lists
    """

    for item in dict_gen:
        yield list(item.values())
