#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareGrid"
  "edwareBreadcrumbs"
  "edwareHeader"
  "text!edwareAssessmentDropdownViewSelectionTemplate"
  "edwareFeedback"
  "edwareUtil"
  "edwareFooter"
  "text!edwareLOSHeaderConfidenceLevelBarTemplate"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareHeader, edwareAssessmentDropdownViewSelectionTemplate, edwareFeedback, edwareUtil, edwareFooter, edwareLOSHeaderConfidenceLevelBarTemplate) ->

  assessmentsData = {}
  studentsConfig = {}
  subjectsData = {}
  
  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    options =
      async: false
      method: "GET"

    edwareDataProxy.getDatafromSource "../data/color.json", options, (defaultColors) ->
      
      getStudentData "/data/list_of_students", params, defaultColors, (assessmentsData, contextData, subjectsData, claimsData, userData, cutPointsData) ->
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
          defaultView = createAssessmentViewSelectDropDown studentsConfig.customViews, cutPointsData
          
          $('#breadcrumb').breadcrumbs(contextData)
          
          renderStudentGrid(defaultView)
          renderHeaderPerfBar(cutPointsData)
          
          # Generate footer links
          $('#footer').generateFooter('list_of_students')
          
          # append user_info (e.g. first and last name)
          if userData
            $('#header .topLinks .user').html edwareUtil.getUserName userData
            role = edwareUtil.getRole userData
            uid = edwareUtil.getUid userData
            edwareFeedback.renderFeedback(role, uid, "list_of_students")
          
  renderHeaderPerfBar = (cutPointsData) ->
    for key of cutPointsData
        items = cutPointsData[key]
        items.bar_width = 120
        
        items.asmt_score_min = assessmentsData["ALL"][0].assessments[key].asmt_score_min
        items.asmt_score_max = assessmentsData["ALL"][0].assessments[key].asmt_score_max
        
        # Last cut point of the assessment
        items.last_interval = items.cut_point_intervals[items.cut_point_intervals.length-1]
      
        items.score_min_max_difference =  items.asmt_score_max - items.asmt_score_min
        
        # Calculate width for first cutpoint
        items.cut_point_intervals[0].asmt_cut_point =  ((items.cut_point_intervals[0].interval - items.asmt_score_min) / items.score_min_max_difference) * items.bar_width
        
        # Calculate width for last cutpoint
        items.last_interval.asmt_cut_point =  ((items.last_interval.interval - items.cut_point_intervals[items.cut_point_intervals.length-2].interval) / items.score_min_max_difference) * items.bar_width
        
        # Calculate width for cutpoints other than first and last cutpoints
        j = 1     
        while j < items.cut_point_intervals.length - 1
          items.cut_point_intervals[j].asmt_cut_point =  ((items.cut_point_intervals[j].interval - items.cut_point_intervals[j-1].interval) / items.score_min_max_difference) * items.bar_width
          j++
        # use mustache template to display the json data  
        output = Mustache.to_html edwareLOSHeaderConfidenceLevelBarTemplate, items
        $("#"+key+"_perfBar").html(output) 
        
    
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
    
    # Add dark border color between Math and ELA section to emphasize the division
    $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(1), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(3), .ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "solid 1px #B1B1B1");

  getStudentData = (sourceURL, params, defaultColors, callback) ->    
    assessmentArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      # # append user_info (e.g. first and last name)
      # if data.user_info
        # $('#header .topLinks .user').html edwareUtil.getUserName data.user_info
        # role = edwareUtil.getRole data.user_info
        # uid = edwareUtil.getUid data.user_info
        # edwareFeedback.renderFeedback(role, uid, "list_of_students")
      assessmentsData = data.assessments
      contextData = data.context
      subjectsData = data.subjects
      claimsData = data.metadata.claims
      cutPointsData = data.metadata.cutpoints
      userData = data.user_info
      
      # if cut points don't have background colors, then it will use default background colors
      for key of cutPointsData
        items = cutPointsData[key]
        
        j = 0
        while j < items.cut_point_intervals.length
          if !items.cut_point_intervals[j].bg_color
            $.extend(items.cut_point_intervals[j], defaultColors[j])
          j++
      
      #  append cutpoints into each individual assessment data
      formatAssessmentsData cutPointsData
      
      if callback
        callback assessmentsData, contextData, subjectsData, claimsData, userData, cutPointsData
      else
        assessmentArray assessmentsData, contextData, subjectsData, claimsData, userData, cutPointsData
      
      
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
  createAssessmentViewSelectDropDown = (customViewsData, cutPointsData)->
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
        renderHeaderPerfBar cutPointsData
        
        # Add dark border color between Math and ELA section to emphasize the division
        if viewName is "Math_ELA"
          $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(1), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(3), .ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "solid 1px #b1b1b1");
        else
          $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(1), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(3), .ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "solid 1px #d0d0d0");
          $('.ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "solid 1px #E2E2E2");
    , ".viewOptions"
    
    # return the first element name as default view
    defaultView = items[0].key
    $("#select_measure_current_view").html $('#' + defaultView).text()
    defaultView
    

  # For each subject, filter out its data
  # Also append cutpoints & colors into each assessment
  formatAssessmentsData = (assessmentCutpoints) ->
    
    # use mustache template to display the json data  
    output = Mustache.to_html edwareLOSHeaderConfidenceLevelBarTemplate, assessmentCutpoints 
      
      
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
          assessment[key].score_bg_color = assessment[key].cut_point_intervals[assessment[key].asmt_perf_lvl-1].bg_color
          assessment[key].score_text_color = assessment[key].cut_point_intervals[assessment[key].asmt_perf_lvl-1].text_color
          # save the assessment to the particular subject
          allAssessments[value.toUpperCase()].push row
    assessmentsData = allAssessments
          
  createStudentGrid: createStudentGrid
