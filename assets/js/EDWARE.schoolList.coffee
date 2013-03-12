#global define
define [
  "jquery"
  "bootstrap"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, bootstrap, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  #
  #    * Create Student data grid
  #    
  createStudentGrid = (params) ->
    
    # Get school data from the server
    getSchoolData "/data/comparing_populations", params, (schoolData, summaryData, subjectsData, colorsData, contextData) ->
      
      # Read Default colors from json
      defaultColors = {}
      options =
        async: false
        method: "GET"
    
      edwareDataProxy.getDatafromSource "../data/color.json", options, (defaultColors) ->
        # Append colors to records and summary section
        # TODO: check if data is not empty, etc first (or do we get a 404?)
        schoolData = appendColorToData schoolData, subjectsData, colorsData, defaultColors
        summaryData = appendColorToData summaryData, subjectsData, colorsData, defaultColors

        getSchoolsConfig "../data/school.json", (schoolConfig, comparePopConfig) ->
          # Change the column name based on the type of report the user is querying for
          reportType = getReportType(params)
          schoolConfig[0].name = comparePopConfig[reportType].name
          schoolConfig[0].options.linkUrl = comparePopConfig[reportType].link
          
          # Render breadcrumbs on the page
          $('#breadcrumb').breadcrumbs(contextData)
          
          # Set the Report title depending on the report that we're looking at
          reportTitle = getReportTitle(contextData, reportType)
          $('#content h4').html 'Comparing ' + reportTitle + ' on Math & ELA'
          
          # Format the summary data for static summary row purposes
          summaryRowName = 'Overall ' + reportTitle + ' Summary'
          summaryData = formatSummaryData(summaryData, summaryRowName)
          
          # Create compare population grid for State/District/School view
          edwareGrid.create "gridTable", schoolConfig, schoolData, summaryData
        
          
          # Show tooltip for population bar on mouseover
          $(".progress").hover ->
            e = $(this)
            e.popover
              html: true
              placement: "top"
              content: ->
                e.find(".progressBar_tooltip").html()
            .popover("show")
          , ->
            e = $(this)
            e.popover("hide")
                  
        
  getSchoolData = (sourceURL, params, callback) ->
    
    dataArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      schoolData = data.records
      summaryData = data.summary
      subjectsData = data.subjects
      colorsData = data.colors
      contextData = data.context
      
      if callback
        callback schoolData, summaryData, subjectsData, colorsData, contextData
      else
        dataArray schoolData, summaryData, subjectsData, colorsData, contextData
      
      
  getSchoolsConfig = (configURL, callback) ->
      
      dataArray = []
            
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource configURL, options, (data) ->
        schoolColumnCfgs = data.schools
        comparePopCfgs = data.comparePopulation
         
        if callback
          callback schoolColumnCfgs, comparePopCfgs
        else
          dataArray schoolColumnCfgs, comparePopCfgs
  
  appendColorToData = (data, subjectsData, colorsData, defaultColors) ->
    
    # Append data with colors
    # records come in as an array, whereas summary doesn't 
    isArray = false
    if data instanceof Array
      recordsLen = data.length
      isArray = true
    else
      recordsLen = 1
    for k of subjectsData
      j = 0
      while (j < recordsLen)
        if isArray
          data[j]['results'][k].intervals = appendColor data[j]['results'][k].intervals, colorsData[k], defaultColors
        else
          data['results'][k].intervals = appendColor data['results'][k].intervals, colorsData[k], defaultColors
        j++
    data
  
  appendColor = (intervals, colorsData, defaultColors) ->
    i = 0
    len = intervals.length
    colorsData = JSON.parse(colorsData)
    while (i < len)
      element = intervals[i]
      if colorsData[i]
        element.color = colorsData[i]
      else
        element.color = defaultColors[i]
      i++
    intervals

  formatSummaryData = (summaryData, summaryRowName) ->
    # Format the summary data for summary row rendering purposes
    data = {}
    for k of summaryData.results
      name = 'results.' + k + '.total'
      data[name] = summaryData.results[k].total
    data['subtitle'] = 'Reference Point'
    data['header'] = true
    data['results'] = summaryData.results
    data['name'] = summaryRowName
    data
    
  getReportTitle = (contextData, reportType) ->
    # Returns the overall summary row name based on the type of report
    map =
      state: 0
      district: 1
      school: 2    
    
    data = ''
    if reportType is 'state'
      data = contextData.items[map[reportType]].id + ' Districts'
    else if reportType is 'district'
      data = contextData.items[map[reportType]].name + ' Schools'
    else if reportType is 'school'
      data = contextData.items[map[reportType]].name + ' Grades'
    data
      

  getReportType = (params) ->
    type = null
    # convert to lower case first
    lowerCaseParams = {}
    for k, v of params
      name = k.toLowerCase()
      lowerCaseParams[name] = v
    if lowerCaseParams['schoolid']
      type = 'school'
    else if lowerCaseParams['districtid']
      type = 'district'
    else if lowerCaseParams['stateid']
      type = 'state'
    type
            
  createStudentGrid: createStudentGrid
  