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

import os

from distutils.core import run_setup

here = os.path.abspath(os.path.dirname(__file__))

dependencies = [
    'edcore',
    'edschema',
    'edapi',
    'edauth',
    'edworker',
    'smarter_common']


for dependency in dependencies:
    pkg_path = os.path.abspath(here + "/../" + dependency + "/")
    os.chdir(pkg_path)
    run_setup("setup.py")
    os.chdir(here)
run_setup("setup.py")
