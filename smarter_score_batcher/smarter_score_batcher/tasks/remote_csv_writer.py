# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from smarter_score_batcher.celery import celery
from smarter_score_batcher.processing.file_processor import generate_csv_from_xml
from smarter_score_batcher.error.exceptions import TSBException
from smarter_score_batcher.error.error_handler import handle_error


@celery.task(name="tasks.tsb.remote_csv_writer")
def remote_csv_generator(meta, csv_file_path, xml_file_path, work_dir, metadata_queue):
    '''
    celery task to generate csv from given xml path
    :param csv_file_path: csv file path
    :param xml_file_path: xml file path
    :returns: True when file is written
    '''
    rtn = False
    try:
        mode = 0o700
        rtn = generate_csv_from_xml(meta, csv_file_path, xml_file_path, work_dir, metadata_queue, mode=mode)
    except TSBException as e:
        # all TSB exception should be caught in here
        e.err_input = 'student_guid: ' + meta.student_id
        handle_error(e, meta.state_code, meta.asmt_id)
    return rtn
