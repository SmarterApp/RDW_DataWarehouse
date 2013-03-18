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
    
    getStudentData "/data/list_of_students", params, (assessmentsData, contextData) ->
      
      getStudentsConfig "../data/student.json", (studentsConfig) ->
        $('#breadcrumb').breadcrumbs(contextData)
        
        edwareGrid.create "gridTable", studentsConfig, assessmentsData
        
        
  getStudentData = (sourceURL, params, callback) ->
    
    assessmentArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      # append user_info (e.g. first and last name)
      if data.user_info
        $('#header .topLinks .user').html data.user_info._User__info.name.firstName + ' ' + data.user_info._User__info.name.lastName
      assessmentsData = data.assessments
      contextData = data.context
      
      if callback
        callback assessmentsData, contextData
      else
        assessmentArray assessmentsData, contextData
      
      
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
  