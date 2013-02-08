#global define
define [
  "jquery"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareUtil"
], ($, edwareDataProxy, edwareGrid, edwareUtil) ->
  
  assessmentsData = []
  assessmentsCutPoints = []
  assessmentCutpoints = {}
   
  #
  #    * Create Student data grid
  #    
      
  createStudentGrid = ->
      
    getStudentData "/data/list_of_students", (assessmentsData, assessmentCutpoints) ->
      
      getStudentsConfig "../data/student.json", (studentsConfig) ->
        edwareGrid.create "gridTable", studentsConfig, assessmentsData, assessmentCutpoints
        
        
  getStudentData = (sourceURL, callback) ->
    
    assessmentArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    params = edwareUtil.getUrlParams()
    
    params.districtId = parseInt(params.districtId)
    params.schoolId = parseInt(params.schoolId)
    
    edwareDataProxy.getDatafromSource sourceURL, params, (data) ->
      assessmentsData = data.assessments
      assessmentsCutPoints = data.cutpoints
      
      if callback
        callback assessmentsData, assessmentsCutPoints
      else
        assessmentArray assessmentsData, assessmentsCutPoints
      
      
  getStudentsConfig = (configURL, callback) ->
      studentColumnCfgs = {}
      
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      edwareDataProxy.getConfigs configURL, (data) ->
        studentColumnCfgs = data
         
        if callback
          callback studentColumnCfgs
        else
          studentColumnCfgs

  createStudentGrid()
  