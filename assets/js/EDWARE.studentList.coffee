#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
  "text!edwareAssessmentDropdownViewSelectionTemplate"
  "cs!edwareFeedback"
  "cs!edwareUtil"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareAssessmentDropdownViewSelectionTemplate, edwareFeedback, edwareUtil) ->

  assessmentsData = {}
  studentsConfig = {}
  subjectsData = {}
  
  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    getStudentData "/data/list_of_students", params, (assessmentsData, contextData, subjectsData, claimsData) ->
      # set school name as the page title from breadcrumb
      $("#school_name").html contextData.items[2].name
      
      getStudentsConfig "../data/student.json", (callback_studentsConfig) ->
        studentsConfig = callback_studentsConfig
        # Use mustache template to replace text in json config
        if assessmentsData['ALL'].length > 0
          # Add assessments data there so we can get column names
          combinedData = subjectsData
          combinedData.claims =  claimsData
          output = Mustache.render(JSON.stringify(studentsConfig), combinedData)
          studentsConfig = JSON.parse(output)
        
        # populate select view
        defaultView = createAssessmentViewSelectDropDown studentsConfig.customViews
        
        $('#breadcrumb').breadcrumbs(contextData)
        
        renderStudentGrid(defaultView)
        $('#content .surveyMonkeyPopup').renderFeedback("teacher", "list_of_students")
        
        # Survey monkey popup
        $("#feedback").popover
          html: true
          placement: "top"
          container: "footer"
          title: ->
              '<div class="pull-right"><button class="btn" id="close" type="button" onclick="$(&quot;#feedback&quot;).popover(&quot;hide&quot;);">Hide</button></div><div class="lead">Survery Monkey</div>'
          template: '<div class="popover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
          content: ->
            $(".surveyMonkeyPopup").html()
        
  renderStudentGrid = (viewName)->
    $("#gbox_gridTable").remove()
    $("#content").append("<table id='gridTable'></table>")
    # Reset the error message, in case previous view shows an error
    edwareUtil.displayErrorMessage ""
    dataName = viewName.toUpperCase()
    # If the view name is not one of the subjects, default it to the default assessments data
    if not (dataName of assessmentsData)
      dataName = 'ALL'
    edwareGrid.create "gridTable", studentsConfig[viewName], assessmentsData[dataName]

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
        uid = edwareUtil.getUid data.user_info
        edwareFeedback.renderFeedback(role, uid, "list_of_students")
      assessmentsData = data.assessments
      contextData = data.context
      subjectsData = data.subjects
      claimsData = data.metadata.claims
      
      #  append cutpoints into each individual assessment data
      formatAssessmentsData data.metadata.cutpoints
      
      if callback
        callback assessmentsData, contextData, subjectsData, claimsData
      else
        assessmentArray assessmentsData, contextData, subjectsData, claimsData
      
      
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

  # creating the assessment view drop down
  createAssessmentViewSelectDropDown = (customViewsData)->
    items = []
    for key of customViewsData
      value = customViewsData[key]
      items.push({'key': key, 'value': value})

    output = Mustache.to_html edwareAssessmentDropdownViewSelectionTemplate, {'items': items}

    $("#content #select_measure").append output
    
    # add event to change view for aseessment
    $(document).on
     click: (e) ->
        e.preventDefault()
        viewName = $(this).attr "id"
        $("#select_measure_current_view").html $('#' + viewName).text()
        renderStudentGrid viewName
    , ".viewOptions"
    
    # return the first element name as default view
    defaultView = items[0].key
    $("#select_measure_current_view").html $('#' + defaultView).text()
    defaultView
    

  # For each subject, filter out its data
  # Also append cutpoints & colors into each assessment
  formatAssessmentsData = (assessmentCutpoints) ->
    # We keep a set of data for each assessment subject
    allAssessments = {'ALL': assessmentsData}
    for key, value of subjectsData
      allAssessments[value.toUpperCase()] = []
    
    for row in allAssessments["ALL"]
      assessment = row['assessments']
      for key, value of subjectsData
        # check that we have such assessment first, since a student may not have taken it
        if key of assessment
          cutpoint = assessmentCutpoints[key]
          $.extend assessment[key], cutpoint
          assessment[key].score_color = assessment[key].cut_point_intervals[assessment[key].asmt_perf_lvl-1].bg_color
          # save the assessment to the particular subject
          allAssessments[value.toUpperCase()].push row
    assessmentsData = allAssessments
          
  createStudentGrid: createStudentGrid
