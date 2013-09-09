require ["EDWARE.comparingPopulations", "edwareFilter", "edwareDataProxy"], (edwareComparingPopulations,edwareFilter, edwareDataProxy) ->
  # Create population grid
  populationGrid = new edwareComparingPopulations.PopulationGrid()

  # Add filter to the page
  configs = {}

  ( () ->
    options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
        configs = data
  )()
  # TODO: move config to filter widget
  filter = $('#cpopFilter').edwareFilter $('.filter_label'), configs, (param)->
    populationGrid.reload(param)
  filter.loadReport()