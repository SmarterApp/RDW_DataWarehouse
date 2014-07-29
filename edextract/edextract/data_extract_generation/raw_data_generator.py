__author__ = 'sravi'

'''
This module contains the logic to gather raw xml files to output directory for archiving
'''

import logging
import os
from edcore.database.edcore_connector import EdCoreDBConnection
from edcore.utils.file_utils import generate_file_path
from edextract.status.constants import Constants
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from edextract.utils.file_utils import File
from edextract.utils.metadata_reader import MetadataReader
import copy

logger = logging.getLogger(__name__)


def generate_raw_data_xml(tenant, output_paths, task_info, extract_args):
    '''
    Write raw xml data to output file

    @param tenant: Requestor's tenant ID
    @param output_paths: list of output path name's to place the selected raw data xml files
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_raw_data_xml
    '''
    query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    root_dir = extract_args[TaskConstants.ROOT_DIRECTORY]
    if type(output_paths) is not list:
        output_paths = [output_paths]

    with EdCoreDBConnection(tenant=tenant) as connection:
        # Get results (streamed, it is important to avoid memory exhaustion)
        results = connection.get_streaming_result(query)
        _copy_files(root_dir, results, output_paths)
        # Done
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _get_path_to_raw_xml(root_dir, **kwargs):
    return generate_file_path(root_dir, "xml", **kwargs)


def _prepare_file_list(raw_root_dir, results):
    metadata_reader = MetadataReader()
    files = []
    for result in results:
        path = _get_path_to_raw_xml(raw_root_dir, **result)
        size = metadata_reader.get_size(path)
        file = File(path, size)
        files.append(file)
    return files


def _copy_files(raw_root_dir, results, output_dirs):
    _output_dirs = copy.deepcopy(output_dirs)
    if type(_output_dirs) is not list:
        _output_dirs = [_output_dirs]
    files = _prepare_file_list(raw_root_dir, results)
    number_of_dirs = len(_output_dirs)
    threshold_size = -1
    if number_of_dirs > 1:
        total_file_size = sum(file.size for file in files)
        threshold_size = int(total_file_size / len(_output_dirs))
    out_dir = _output_dirs.pop(0)
    current_total_size = 0
    for file in files:
        if threshold_size > 0 and current_total_size + file.size > threshold_size and _output_dirs:
            out_dir = _output_dirs.pop(0)
            current_total_size = 0
        os.symlink(file.name, os.path.join(out_dir, os.path.basename(file.name)))
        current_total_size += file.size
