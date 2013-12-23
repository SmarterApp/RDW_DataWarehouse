require [
  "EDWARE.comparingPopulations"
  "edwareFilter"
  "edwareDataProxy"
  "edwareConstants"
], (edwareComparingPopulations,edwareFilter, edwareDataProxy, Constants) ->

  reportName = Constants.REPORT_JSON_NAME.CPOP

  edwareDataProxy.getDataForReport(reportName).done (reportConfig) ->
    # Create population grid
    populationGrid = new edwareComparingPopulations.PopulationGrid(reportConfig)
    # Add filter to the page
    edwareDataProxy.getDataForFilter().done (filterConfigs) ->
      # move config to filter widget
      filter = $('#cpopFilter').edwareFilter '.filterItem', filterConfigs, (param)->
        populationGrid.reload param
      populationGrid.setFilter filter
      filter.loadReport()
