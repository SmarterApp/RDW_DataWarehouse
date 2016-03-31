###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

define ["jquery"], ($) ->

  # define namespace
  # TODO: we don't use this object from the beginning, maybe we should start using it
  EDWARE = EDWARE or {}

  EDWARE

  # bug from wkhtmltopdf causes issue when we use bind https://github.com/masayuki0812/c3/issues/552
  Function::bind = Function::bind or (thisp) ->
    fn = this
    ->
      fn.apply thisp, arguments
