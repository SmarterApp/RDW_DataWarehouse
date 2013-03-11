#global define
define [
  "jquery"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  
  assessmentsData = []
  assessmentsCutPoints = []
  assessmentCutpoints = {}
   

  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    # Get school data from the server
    getSchoolData "/data/comparing_populations", params, (schoolData, summaryData, subjectsData, colorsData, contextData) ->
      
      # Get school grid column configs
      getSchoolsConfig "../data/school.json", (schoolConfig) ->
    
        $('#breadcrumb').breadcrumbs(contextData)
        edwareGrid.create "gridTable", schoolConfig, schoolData, summaryData
        
        
  getSchoolData = (sourceURL, params, callback) ->
    
    dataArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      schoolData = data.records
      summaryData = data.summary
      subjectsData = data.subjects
      colorsData = data.colors
      contextData = data.context
      
      if callback
        callback schoolData, summaryData, subjectsData, colorsData, contextData
      else
        dataArray schoolData, summaryData, subjectsData, colorsData, contextData
      
      
  getSchoolsConfig = (configURL, callback) ->
      schoolColumnCfgs = {}
      
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource configURL, options, (data) ->
        schoolColumnCfgs = data.schools
         
        if callback
          callback schoolColumnCfgs
        else
          schoolColumnCfgs


  createStudentGrid: createStudentGrid
  