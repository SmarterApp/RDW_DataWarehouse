#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  
  assessmentsData = []
  
  #
  #    * Create Compare population data grid
  #    
  createComparePopulationGrid = (params) ->
    
    getDistrictData "/data/comparing_populations", params, (districtData, summaryData, subjectsData, colorsData, contextData) ->
      $('#breadcrumb').breadcrumbs(contextData)
  #TODO: reuse the one from school and state
  
  getDistrictData = (sourceURL, params, callback) ->
    
    dataArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      districtData = data.records
      summaryData = data.summary
      subjectsData = data.subjects
      colorsData = data.colors
      contextData = data.context
      
      if callback
        callback districtData, summaryData, subjectsData, colorsData, contextData
      else
        dataArray districtData, summaryData, subjectsData, colorsData, contextData
  
      
  createComparePopulationGrid: createComparePopulationGrid