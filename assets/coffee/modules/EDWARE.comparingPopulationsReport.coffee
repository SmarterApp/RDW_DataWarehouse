require [
  "edware"
  "edwareComparingPopulations"
  "edwareFilter"
  "edwareDataProxy"
  "edwareConstants"
  "edwarePreferences"
], (edware, edwareComparingPopulations,edwareFilter, edwareDataProxy, Constants, edwarePreferences) ->

  reportName = Constants.REPORT_JSON_NAME.CPOP

  edwareDataProxy.getDataForReport(reportName).done (reportConfig) ->
    # Create population grid
    populationGrid = new edwareComparingPopulations.PopulationGrid(reportConfig)
    # Add filter to the page
    edwareDataProxy.getDataForFilter().done (filterConfigs) ->
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
