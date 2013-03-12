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
        schoolData = appendColorToData schoolData, subjectsData, colorsData, defaultColors
        summaryData = appendColorToData summaryData, subjectsData, colorsData, defaultColors, 1

        getSchoolsConfig "../data/school.json", (schoolConfig, comparePopConfig) ->
          # Change the column name based on the type of report the user is querying for
          reportType = getReportType(params)
          schoolConfig[0].name = comparePopConfig[reportType].name
          schoolConfig[0].options.linkUrl = comparePopConfig[reportType].link
          
          $('#breadcrumb').breadcrumbs(contextData)
          # Format the summary data for static summary row purposes
          formmatedSummary = formatSummaryData(summaryData)
          edwareGrid.create "gridTable", schoolConfig, schoolData, formmatedSummary
        
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
  
  appendColorToData = (data, subjectsData, colorsData, defaultColors, resultLen) ->
    
    # Append data with colors
    if !resultLen
      recordsLen = data.length
    else
      recordsLen = resultLen
    for k of subjectsData
      j = 0
      while (j < recordsLen)
        if !resultLen
          data[j]['results'][k].intervals = appendColor data[j]['results'][k].intervals, colorsData[k], defaultColors
        else
          data['results'][k].intervals = appendColor data['results'][k].intervals, colorsData[k], defaultColors
        j++
    data
  
  appendColor = (intervals, colorsData, defaultColors) ->
    i = 0
    len = intervals.length
    colorsData = JSON.parse(colorsData)
    # For now, ignore everything behind the 4th interval
    if len > 4
      intervals = intervals[0..3]
      len = intervals.length
    while (i < len)
      element = intervals[i]
      if colorsData[i]
        element.color = colorsData[i]
      else
        element.color = defaultColors[i]
      i++
    intervals

  formatSummaryData = (summaryData) ->
    data = {}
    for k of summaryData.results
      name = 'results.' + k + '.total'
      data[name] = summaryData.results[k].total
    data['subtitle'] = 'Reference Point'
    data['name'] = 'Overall Summary'
    data['header'] = true
    data['results'] = summaryData.results
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
  