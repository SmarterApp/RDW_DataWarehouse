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
      
      breadcrumbsData = {}
        
      edwareUtil.readJson "../data/list_of_students_breadcrumbs.json", (tempData) ->
        breadcrumbsData = tempData
        
        
      arr = breadcrumbsData['items']
      length = arr.length
      element = null
      i = 0
      
      while i < length
        element = arr[i]
        element.name = contextData[element.field_name]
        i++
      
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
          
  #
  #    * Get breadcrumbs data
  # 
  # readBreadcrumbs = (templateURL, callback) ->
      # return false if templateURL is "undefined" or typeof templateURL is "number" or typeof templateURL is "function" or typeof templateURL is "object"
#         
      # $.ajax
        # url: templateURL
        # dataType: "json"
        # async: false
        # success: (data) ->
          # content = data
# 
          # if callback
            # callback content
          # else
            # content

  createStudentGrid: createStudentGrid
  