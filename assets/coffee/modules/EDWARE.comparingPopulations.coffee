#global define
define [
  "jquery"
  "bootstrap"
  "edwareDataProxy"
  "edwareGrid"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareFooter"
], ($, bootstrap, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareFooter) ->
  
  myCustomSort1 = (cell, rowObject) ->
      percent = rowObject.results.subject1.intervals[0].percentage
      
  myCustomSort2 = (cell, rowObject) ->
      percent = rowObject.results.subject1.intervals[1].percentage     
      
  myCustomSort3 = (cell, rowObject) ->
      percent = rowObject.results.subject1.intervals[3].percentage
  
  # Add header to the page
  edwareUtil.getHeader()
  #
  #    * Create Student data grid
  #    
  createPopulationGrid = (params) ->
    
    # Get school data from the server
    getPopulationData "/data/comparing_populations", params, (populationData, summaryData, asmtSubjectsData, colorsData, breadcrumbsData, user_info) ->
      
      # Read Default colors from json
      defaultColors = {}
      options =
        async: false
        method: "GET"
    
      edwareDataProxy.getDatafromSource "../data/common.json", options, (data) ->
        defaultColors = data.colors
        feedbackData = data.feedback
        breadcrumbsConfigs = data.breadcrumb
        reportInfo = data.reportInfo
        gridConfig = data.comparingPopulations.grid
        customViews = data.comparingPopulations.customViews
        # # append user_info (e.g. first and last name)
        if user_info
          $('#header .topLinks .user').html edwareUtil.getUserName user_info
          
        # Determine if the report is state, district or school view
        reportType = getReportType(params)
        
        # Append colors to records and summary section
        # Do not format data, or get breadcrumbs if the result is empty
        if populationData.length > 0
          populationData = appendColorToData populationData, asmtSubjectsData, colorsData, defaultColors
          summaryData = appendColorToData summaryData, asmtSubjectsData, colorsData, defaultColors

          # Change the column name and link url based on the type of report the user is querying for
          gridConfig[0].items[0].name = customViews[reportType].name
          gridConfig[0].items[0].options.linkUrl = customViews[reportType].link
          gridConfig[0].items[0].options.id_name = customViews[reportType].id_name
          
          if customViews[reportType].name is "Grade"
            gridConfig[0].items[0].sorttype = "int"
          
          # Render breadcrumbs on the page
          $('#breadcrumb').breadcrumbs(breadcrumbsData, breadcrumbsConfigs)
          
          # Set the Report title depending on the report that we're looking at
          reportTitle = getReportTitle(breadcrumbsData, reportType)
          alignmentButton = "<div><button type='button' class='btn btn-primary' id='barAlignment' data-toggle='button'>Single Toggle</button></div>"
          $('#content h2').html reportTitle + alignmentButton
          
          # Format the summary data for summary row purposes
          summaryRowName = getOverallSummaryName(breadcrumbsData, reportType)
          summaryData = formatSummaryData(summaryData, summaryRowName)
          
        # Create compare population grid for State/District/School view
        edwareGrid.create "gridTable", gridConfig, populationData, summaryData
        
        # Generate footer
        $('#footer').generateFooter('comparing_populations', reportInfo)
        
        # # append user_info (e.g. first and last name)
        if user_info
          role = edwareUtil.getRole user_info
          uid = edwareUtil.getUid user_info
          edwareUtil.renderFeedback(role, uid, "comparing_populations_" + reportType, feedbackData)
      
        # Show tooltip for population bar on mouseover
        $(document).on
          mouseenter: ->
            e = $(this)
            e.popover
              html: true
              placement: "top"
              trigger: "manual"
              template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
              content: ->
                e.find(".progressBar_tooltip").html() # template location: widgets/populatoinBar/template.html
            .popover("show")
          click: (e) ->
            e.preventDefault()
          mouseleave: ->
            e = $(this)
            e.popover("hide")
        , ".progress"
        
        grid = $("#gridTable")
        cm = grid.getGridParam("colModel")[2];
        $("#sort1").click ->
          cm.sorttype = myCustomSort1
          grid.trigger("reloadGrid")
          
        $("#sort2").click ->
          cm.sorttype = myCustomSort2
          grid.trigger("reloadGrid")
            
        $("#sort3").click ->
          cm.sorttype = myCustomSort3
          grid.trigger("reloadGrid")
          
        $("#barAlignment").click ->
          $(".populationBar").css("width", "200px")
        
        $('.dropdown-toggle').dropdown()
                    
  # Get population data from server       
  getPopulationData = (sourceURL, params, callback) ->
    
    dataArray = []
    
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    options =
      async: true
      method: "POST"
      params: params
  
    edwareDataProxy.getDatafromSource sourceURL, options, (data) ->
      populationData = data.records
      summaryData = data.summary
      asmtSubjectsData = data.subjects
      colorsData = data.colors
      breadcrumbsData = data.context
      user_info = data.user_info
      
      if callback
        callback populationData, summaryData, asmtSubjectsData, colorsData, breadcrumbsData, user_info
      else
        dataArray populationData, summaryData, asmtSubjectsData, colorsData, breadcrumbsData, user_info
      
  # Returns column configurations for population grid   
  getColumnConfig = (configURL, callback) ->
      
      dataArray = []
            
      return false  if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
      
      options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource configURL, options, (data) ->
        schoolColumnCfgs = data.grid
        comparePopCfgs = data.customViews
         
        if callback
          callback schoolColumnCfgs, comparePopCfgs
        else
          dataArray schoolColumnCfgs, comparePopCfgs
          
  # Traverse through to intervals to prepare to append color to data
  appendColorToData = (data, asmtSubjectsData, colorsData, defaultColors) ->
    for k of asmtSubjectsData
      j = 0
      while (j < data.length)
        data[j]['results'][k].intervals = appendColor data[j]['results'][k].intervals, colorsData[k], defaultColors
        j++
    data
  
  # Add color for each intervals
  appendColor = (intervals, colorsData, defaultColors) ->
    i = 0
    len = intervals.length
    while (i < len)
      element = intervals[i]
      if colorsData and colorsData[i]
        element.color = colorsData[i]
      else
        element.color = defaultColors[i]
        
      # if percentage is less than 9 then remove the percentage text from the bar
      if element.percentage > 9
        element.showPercentage = true
      else
        element.showPercentage = false
      
      # format nubmers
      element.count = formatNumber element.count
      i++
    intervals
    
  # Add comma as thousand separator to numbers
  # Return 0 if parameter is undefined
  formatNumber = (num) ->
    if num then num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") else 0
  
  # Format the summary data for summary row rendering purposes
  formatSummaryData = (summaryData, summaryRowName) ->
    data = {}
    summaryData = summaryData[0]
    for k of summaryData.results
      name = 'results.' + k + '.total'
      data[name] = summaryData.results[k].total
    data['subtitle'] = 'Reference Point'
    # Set header row to be true to indicate that it's the summary row
    data['header'] = true
    data['results'] = summaryData.results
    data['name'] = summaryRowName
    data
 
  # Returns report title based on the type of report
  getReportTitle = (breadcrumbsData, reportType) ->
    if reportType is 'state'
      data = addApostropheS(breadcrumbsData.items[0].name) + ' Districts'
    else if reportType is 'district'
      data = addApostropheS(breadcrumbsData.items[1].name) + ' Schools'
    else if reportType is 'school'
      data = addApostropheS(breadcrumbsData.items[2].name) + ' Grades'
    'Comparing '+ data + ' on Math & ELA'
      
  # Returns the overall summary row name based on the type of report
  getOverallSummaryName = (breadcrumbsData, reportType) ->
    if reportType is 'state'
      data = breadcrumbsData.items[0].name + ' District'
    else if reportType is 'district'
      data = breadcrumbsData.items[1].name + ' School'
    else if reportType is 'school'
      data = breadcrumbsData.items[2].name + ' Grade'
    'Overall ' + data + ' Summary'
    
  # Add an 's to a word
  addApostropheS = (word) ->
    if word.substr(word.length - 1) is "s"
      word = word + "'"
    else
      word = word + "'s"
    word
    
  # Based on query parameters, return the type of report that the user is requesting for
  getReportType = (params) ->
    if params['schoolGuid']
      reportType = 'school'
    else if params['districtGuid']
      reportType = 'district'
    else if params['stateCode']
      reportType = 'state'
    reportType
            
  createPopulationGrid: createPopulationGrid
  