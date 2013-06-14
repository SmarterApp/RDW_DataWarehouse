require ["../main"], (common) ->
  require ["EDWARE.comparingPopulations"], (edwareComparingPopulations) ->
    getUrlParams = ->
      params = {}
      window.location.search.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
        params[key] = value
    
      params
    params = getUrlParams()
    edwareComparingPopulations.createPopulationGrid params

