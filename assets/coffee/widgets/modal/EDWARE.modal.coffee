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

  lastFocus = undefined

  $.fn.edwareModal = (options) ->
    # flag to indicate whether current modal resets last focused
    # element in the page
    resetLastFocus = true unless options?.keepLastFocus
    # bind events when initialize
    if not options or typeof(options) is 'object'
      # remember last focus
      this.on 'show', ->
        lastFocus = document.activeElement if resetLastFocus
      # restore last focus
      this.on 'hidden', ->
        lastFocus.focus() if lastFocus
    this.modal options
