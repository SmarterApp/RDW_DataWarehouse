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

require [
  "edwareEvents"
  "edwareComparingPopulations"
  "edwareFilter"
  "edwareDataProxy"
  "edwareConstants"
  "edwarePreferences"
], (edwareEvents, edwareComparingPopulations,edwareFilter, edwareDataProxy, Constants, edwarePreferences) ->

  reportName = Constants.REPORT_JSON_NAME.CPOP

  edwareDataProxy.getDataForReport(reportName).done (reportConfig) ->
    # Create population grid
    populationGrid = new edwareComparingPopulations.PopulationGrid(reportConfig)

    edwarePreferences.saveQuickLinksSchoolBound reportConfig.quickLinksSchoolRollupBound
    edwarePreferences.saveQuickLinksDistrictBound reportConfig.quickLinksDistrictRollupBound

    # Add filter to the page
    edwareDataProxy.getDataForFilter().done (filterConfigs) ->
      # The funky while looping because splicing an array while you're for..looping
      # it isn't a good idea
      filters = filterConfigs.filters
      index = filters.length - 1
      while index >= 0
        if filters[index] and filters[index].interimOnly
            filters.splice(index, 1)
        index--
      # move config to filter widget
      filter = $('#cpopFilter').edwareFilter '.filterItem', filterConfigs, (param)->
        param = mergeWithPreference(param)
        populationGrid.reload param
      populationGrid.setFilter filter
      filter.loadReport()

  # reset assessment type
  # TODO this line of code should be changed after merging asmt year with asmt object in LOS
  edwarePreferences.clearAsmtPreference()

  mergeWithPreference = (params)->
    edwarePreferences.saveStateCode params['stateCode']
    asmtYear = edwarePreferences.getAsmtYearPreference()
    params['asmtYear'] = asmtYear if asmtYear
    params
