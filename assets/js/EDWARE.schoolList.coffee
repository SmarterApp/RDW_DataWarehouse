#global define
define [
  "jquery"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
], ($, edwareDataProxy, edwareGrid, edwareBreadcrumbs) ->
  
  assessmentsData = []
  assessmentsCutPoints = []
  assessmentCutpoints = {}
   

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
        
        schoolData = appendColorToData schoolData, subjectsData, colorsData, defaultColors, "results"
        summaryData = appendColorToData summaryData, subjectsData, colorsData, defaultColors, null, 1

        getSchoolsConfig "../data/school.json", (schoolConfig) ->
          $('#breadcrumb').breadcrumbs(contextData)
          edwareGrid.create "gridTable", schoolConfig, schoolData, summaryData
        
        
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
      schoolColumnCfgs = {}
      
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource configURL, options, (data) ->
        schoolColumnCfgs = data.schools
         
        if callback
          callback schoolColumnCfgs
        else
          schoolColumnCfgs
  
  appendColorToData = (data, subjectsData, colorsData, defaultColors, nodeName, resultLen) ->
    # Append data with colors
    if !resultLen
      recordsLen = data.length
    for k of subjectsData
      j = 0
      while (j < recordsLen)
        if nodeName
          node = data[j][nodeName][k].intervals
        else
          node = data[k].intervals  
        node = appendColor node, colorsData[k], defaultColors
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

  createStudentGrid: createStudentGrid
  