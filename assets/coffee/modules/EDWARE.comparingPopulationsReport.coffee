require ["../main"], (common) ->
  require ["EDWARE.comparingPopulations", "edwareUtil"], (edwareComparingPopulations, edwareUtil) ->
    params = edwareUtil.getUrlParams()
    edwareComparingPopulations.createPopulationGrid params

