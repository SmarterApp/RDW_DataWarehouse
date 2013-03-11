#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  
  #
  #    * Create Compare population data grid
  #    
  createComparePopulationGrid = (params) ->
    
    getStateData "/data/comparing_populations", params, (data, contextData) ->
      $('#breadcrumb').breadcrumbs(contextData)
  
  getStateData = (sourceURL, params, callback) ->
    
    dataArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      data = data
      contextData = data.context
      
      if callback
        callback data, contextData
      else
        dataArray data, contextData
      
  createComparePopulationGrid: createComparePopulationGrid