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

  assessmentsData = []
  studentsConfig = {}
  subjectsData = {}
   

  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    getStudentData "/data/list_of_students", params, (assessmentsData, contextData, subjectsData) ->
      # set school name
      setSchoolName contextData.items[2].name
      
      getStudentsConfig "../data/student.json", (callback_studentsConfig) ->
        studentsConfig = callback_studentsConfig
        # Use mustache template to replace text in json config
        if assessmentsData.length > 0
          # Add assessments data there so we can get column names
          combinedData = subjectsData
          combinedData.assessments =  assessmentsData[0].assessments
          output = Mustache.render(JSON.stringify(studentsConfig), combinedData)
          studentsConfig = JSON.parse(output)
        
        # populate select view
        defaultView = createStudentsConfigViewSelect studentsConfig.customViews
        
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
    $("#content #select_measure .btn-group .btn.dropdown-toggle #select_measure_current_view").html $('#' + viewName).text()
    edwareGrid.create "gridTable", studentsConfig[viewName], assessmentsData

        
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

  setSchoolName = (schoolName)->
    $("#school_name").html schoolName

  createStudentsConfigViewSelect = (customViewsData)->
    items = []
    for key of customViewsData
      value = customViewsData[key]
      items.push({'key': key, 'value': value})

    output = Mustache.to_html edwareAssessmentDropdownViewSelectionTemplate, {'items': items}

    $("#content #select_measure").append output
    
    # add event
    $(document).on
     click: (e) ->
        e.preventDefault()
        renderStudentGrid $(this).attr "id"
    , ".viewOptions"
    
    # return the first element name as default view
    items[0].key

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
  