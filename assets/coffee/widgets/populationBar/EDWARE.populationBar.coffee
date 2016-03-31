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

define [
  'jquery'
  "mustache"
  "edwareUtil"
  "text!edwarePopulationBarTemplate"
], ($, Mustache, edwareUtil, populationBarTemplate) ->
  #
  #    * Population level bar widget
  #    * Generate confidence level bar and calculate cutpoint pixel width, score position, score interval position
  #
  @isPublic=edwareUtil.isPublicReport()
  $.fn.populationBar = (items) ->
    output = renderPopulationBar items
    this.html output

  renderPopulationBar = (items) ->
    rightTotalPercentage = items.sortedValue
    leftTotalPercentage = 100 - rightTotalPercentage
    if rightTotalPercentage > 0 then items.rightTotalPercentage = rightTotalPercentage
    if leftTotalPercentage > 0 then items.leftTotalPercentage = leftTotalPercentage
    items.isPublic=@isPublic
    # render population bar from template
    output = Mustache.to_html populationBarTemplate, items
    output

  create = (data, container) ->
    if container
      $(container).populationBar data
    else
      renderPopulationBar data

  create: create
