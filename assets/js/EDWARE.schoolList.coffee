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
    
    breadcrumbsData = {}
      
    options =
      async: false
      method: "GET"
    
    edwareDataProxy.getDatafromSource "../data/list_of_students_breadcrumbs.json", options, (tempData) ->
      breadcrumbsData = tempData
      
    # Get school data from the server
    getSchoolsData "../data/schoolData.json", params, (schoolData, summaryData, contextData) ->
      
      # Get school grid column configs
      getSchoolsConfig "../data/school.json", (schoolConfig) ->
        arr = breadcrumbsData['items']
        length = arr.length
        element = null
        i = 0
        
        while i < length
          element = arr[i]
          element.name = contextData[element.field_name]
          i++
          
        $('#breadcrumb').breadcrumbs(breadcrumbsData)
        
        edwareGrid.create "gridTable", schoolConfig, schoolData, summaryData
        
        
  getSchoolsData = (sourceURL, params, callback) ->
    
    assessmentArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      schoolData = data.schoolData
      summaryData = data.summaryData
      contextData = data.context
      
      if callback
        callback schoolData, summaryData, contextData
      else
        assessmentArray schoolData, summaryData, contextData
      
      
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
  