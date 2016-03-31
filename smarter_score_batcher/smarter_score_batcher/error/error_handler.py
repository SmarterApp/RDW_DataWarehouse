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

'''
Created on Sep 23, 2014

@author: tosako
'''
from smarter_score_batcher.error.error_file_generator import build_err_list
from smarter_score_batcher.database.db_utils import save_error_msg


def handle_error(e_TSBException, state_code, asmt_guid):

    err_code = e_TSBException.err_code
    err_source = e_TSBException.err_source
    err_code_text = e_TSBException.err_code_text
    err_source_text = e_TSBException.err_source_text
    err_input = e_TSBException.err_input
    err_list = build_err_list(err_code, err_source, err_code_text, err_source_text, err_input)
    save_error_msg(asmt_guid, state_code, **err_list)
