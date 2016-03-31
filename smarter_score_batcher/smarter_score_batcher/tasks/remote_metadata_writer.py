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
from smarter_score_batcher.utils.metadata_generator import metadata_generator_bottom_up


@celery.task(name="tasks.tsb.remote_metadata_writer")
def metadata_generator_task(file_path):
    metadata_generator_bottom_up(file_path, generateMetadata=True)
