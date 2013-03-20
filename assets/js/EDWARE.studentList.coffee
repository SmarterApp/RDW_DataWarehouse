#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  
  assessmentsData = []
  studentsConfig = {}
  subjectsData = {}
   

  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    getStudentData "/data/list_of_students", params, (assessmentsData, contextData, subjectsData) ->
      
      getStudentsConfig "../data/student.json", (callback_studentsConfig) ->
        studentsConfig = callback_studentsConfig
        # Use mustache template to replace text in json config
        if assessmentsData.length > 0
          # Add assessments data there so we can get column names
          combinedData = subjectsData
          combinedData.assessments =  assessmentsData[0].assessments
          output = Mustache.render(JSON.stringify(studentsConfig), combinedData)
          studentsConfig = JSON.parse(output)
        createStudentsConfigViewSelect studentsConfig.customViews
        
        $('#breadcrumb').breadcrumbs(contextData)
        
        renderStudentGrid()
        


  renderStudentGrid = ->
    $("#gbox_gridTable").remove()
    $("#content").append("<table id='gridTable'></table>")
    view = $("#select_measure").val()
    edwareGrid.create "gridTable", studentsConfig[view], assessmentsData
        
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
      subjectsData = data.subjects
      
      #  append cutpoints into each individual assessment data
      appendCutpointsIntoAssessments data.cutpoints
      
      if callback
        callback assessmentsData, contextData, subjectsData
      else
        assessmentArray assessmentsData, contextData, subjectsData
      
      
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

  # Appends cutpoints & colors into each assessment
  appendCutpointsIntoAssessments = (assessmentCutpoints) ->
    for row in assessmentsData
      assessment = row['assessments']
      for subject of subjectsData
        # check that we have such assessment first, since a student may not have taken it
        if subject of assessment
          cutpoint = assessmentCutpoints[subject]
          assessment[subject].cut_point_intervals = cutpoint

  createStudentGrid: createStudentGrid
  