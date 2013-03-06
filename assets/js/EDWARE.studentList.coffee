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
      
    getStudentData "/data/list_of_students", params, (assessmentsData, assessmentCutpoints, contextData) ->
      
      getStudentsConfig "../data/student.json", (studentsConfig) ->
        arr = breadcrumbsData['items']
        length = arr.length
        element = null
        i = 0
        
        while i < length
          element = arr[i]
          element.name = contextData[element.field_name]
          i++
          
        $('#breadcrumb').breadcrumbs(breadcrumbsData)
        
        edwareGrid.create "gridTable", studentsConfig, assessmentsData, assessmentCutpoints
        
        
  getStudentData = (sourceURL, params, callback) ->
    
    assessmentArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      assessmentsData = data.assessments
      assessmentsCutPoints = data.cutpoints
      contextData = data.context
      
      if callback
        callback assessmentsData, assessmentsCutPoints, contextData
      else
        assessmentArray assessmentsData, assessmentsCutPoints, contextData
      
      
  getStudentsConfig = (configURL, callback) ->
      studentColumnCfgs = {}
      
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource configURL, options, (data) ->
        studentColumnCfgs = data.students
         
        if callback
          callback studentColumnCfgs
        else
          studentColumnCfgs


  createStudentGrid: createStudentGrid
  