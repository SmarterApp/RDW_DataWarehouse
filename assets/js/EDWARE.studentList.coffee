#global define
define [
  "jquery"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareUtil"
  "cs!edwareBreadcrumbs"
], ($, edwareDataProxy, edwareGrid, edwareUtil, edwareBreadcrumbs) ->
  
  assessmentsData = []
  assessmentsCutPoints = []
  assessmentCutpoints = {}
   
  #
  #    * Create Student data grid
  #    
  
  createStudentGrid = (params) ->
    
    getStudentData "/data/list_of_students", params, (assessmentsData, assessmentCutpoints, contextData) ->
      
      breadcrumbsData = 
        { "items": [
          {
            name: contextData['state_name']
            link: "http://www.google.com" 
          },
          {
            name: contextData['district_name']
            link: "http://www.cnn.com" 
          },
          {
            name: contextData['school_name']
            link: "http://www.cnn.com" 
          },
          {
            name: contextData['grade']
          },
        ]}
      
      $('#breadcrumb').breadcrumbs(breadcrumbsData)
      
      getStudentsConfig "../data/student.json", (studentsConfig) ->
        edwareGrid.create "gridTable", studentsConfig, assessmentsData, assessmentCutpoints
        
        
  getStudentData = (sourceURL, params, callback) ->
    
    assessmentArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    edwareDataProxy.getDatafromSource sourceURL, params, (data) ->
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
      
      edwareDataProxy.getConfigs configURL, (data) ->
        studentColumnCfgs = data
         
        if callback
          callback studentColumnCfgs
        else
          studentColumnCfgs

  createStudentGrid: createStudentGrid
  