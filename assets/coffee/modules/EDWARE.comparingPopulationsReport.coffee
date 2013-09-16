require ["EDWARE.comparingPopulations", "edwareFilter", "edwareDataProxy"], (edwareComparingPopulations,edwareFilter, edwareDataProxy) ->
  # Create population grid
  populationGrid = new edwareComparingPopulations.PopulationGrid()

  # Add filter to the page
  configs = {}

  ( () ->
      configs =edwareDataProxy.getDataForFilter()
  )()
  # move config to filter widget
  filter = $('#cpopFilter').edwareFilter $('.filter_label'), configs, (param)->
    populationGrid.reload(param)
  populationGrid.setFilter(filter)
  filter.loadReport()