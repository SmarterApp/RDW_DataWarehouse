#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  
  assessmentsData = []
  assessmentsCutPoints = []
  assessmentCutpoints = {}
  studentsConfig = {}
   

  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    getStudentData "/data/list_of_students", params, (assessmentsData, contextData) ->
      
      getStudentsConfig "../data/student.json", (callback_studentsConfig) ->
        studentsConfig = callback_studentsConfig
        createStudentsConfigViewSelect studentsConfig.customViews
        
        $('#breadcrumb').breadcrumbs(contextData)
        
        renderStudentGrid()
        


  renderStudentGrid = ->
    $("#gbox_gridTable").remove()
    $("#content").append("<table id='gridTable'></table>")
    view = $("#select_measure").val()
    if assessmentsData.length > 0
          output = Mustache.render( JSON.stringify(studentsConfig[view]), assessmentsData[0].assessments)
          updatedStudentsConfig = JSON.parse(output)
    edwareGrid.create "gridTable", updatedStudentsConfig, assessmentsData
        
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
      
        if callback
          callback data
        else
          data


  createStudentsConfigViewSelect = (customViewsData)->
    $("#select_measure").change renderStudentGrid
      
    $.each customViewsData, (key, value) ->
      $("#select_measure").append($("<option></option>").attr("value", key).text(value))


  createStudentGrid: createStudentGrid
  