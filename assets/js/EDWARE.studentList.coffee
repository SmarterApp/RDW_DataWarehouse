#global define
define [
  "jquery"
  "bootstrap"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
  "cs!edwareFeedback"
  "cs!edwareUtil"
], ($, bootstrap, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareFeedback, edwareUtil) ->
  
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
        $('#header .topLinks .user').html edwareUtil.getUserName data.user_info
        role = edwareUtil.getRole data.user_info
        edwareFeedback.renderFeedback(role, "list_of_students")
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
  