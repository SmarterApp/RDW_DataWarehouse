__author__ = 'tshewchuk'

"""
This module contains the logic to write to an Assessment CSV or JSON extract file.
"""

import csv
import json
from edextract.utils.json_formatter import format_json

from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.status.status import ExtractStatus, insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection


def generate_csv(tenant, output_file, task_info, extract_args):
    """
    Write data extract to CSV file.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_csv
    """

    query = extract_args[TaskConstants.TASK_QUERY]

    with EdCoreDBConnection(tenant=tenant) as connection, open(output_file, 'w') as csv_file:
        results = connection.get_streaming_result(query)  # this result is a generator
        csvwriter = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        header = []
        for result in results:
            if len(header) is 0:
                header = list(result.keys())
                csvwriter.writerow(header)
            row = list(result.values())
            csvwriter.writerow(row)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def generate_json(tenant, output_file, task_info, extract_args):
    """
    Write data extract to JSON file.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_json
    """

    query = extract_args[TaskConstants.TASK_QUERY]

    with EdCoreDBConnection(tenant=tenant) as connection, open(output_file, 'w') as json_file:
        results = connection.get_result(query)
        # There should only be one result in the list
        if len(results) is 1:
            formatted = format_json(results[0])
            json.dump(formatted, json_file, indent=4)
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.GENERATED_JSON})
        else:
            insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.FAILED, Constants.INFO: "Results length is: " + str(len(results))})
