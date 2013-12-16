###
# Comparing Population Report #

###

define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareGrid"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareHeader"
  "edwareDropdown"
  "edwareGridStickyCompare"
  "edwarePreferences"
  "edwareConstants"
  "edwareClientStorage"
  "edwareReportInfoBar"
  "edwareReportActionBar"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareHeader, edwareDropdown, edwareStickyCompare, edwarePreferences, Constants, edwareClientStorage, edwareReportInfoBar, edwareReportActionBar) ->

  POPULATION_BAR_WIDTH = 145

  class ConfigBuilder
    ### Grid configuration builder. ###

    constructor: (template, subjects) ->
      ###

      ###
      output = Mustache.render(JSON.stringify(template), subjects)
      this.gridConfig = JSON.parse(output)
      this

    customize: (customView) ->
      firstColumn = this.gridConfig[0].items[0]
      firstColumn.name = customView.name
      firstColumn.exportName = customView.exportName
      firstColumn.options.linkUrl = customView.link
      firstColumn.options.id_name = customView.id_name
      firstColumn.sorttype = "int" if customView.name is "Grade"
      this

    build: ()->
      this.gridConfig


  class PopulationGrid

    constructor: () ->
      configPromise = edwareDataProxy.getDataForReport Constants.REPORT_JSON_NAME.CPOP
      configPromise.done @initialize.bind(@)

    initialize: (config)->
      this.config = config
      this.breadcrumbsConfigs = config.breadcrumb
      this.configTemplate = config.comparingPopulations.grid
      this.customViews = config.comparingPopulations.customViews
      this.labels = config.labels
      this.defaultColors = config.colors
      this.gridContainer = $('.gridHeight100')
      this.gridHeight = window.innerHeight - 312#subtract footer and header height
      edwareUtil.reRenderBody this.labels
      # create align button
      this.alignment = new Alignment('.align_button', @labels)
      # default sort
      this.sort = {
        name: 'name'
        order: 'asc'
        index: 0
      }
      this.stickyCompare = new edwareStickyCompare.EdwareGridStickyCompare this.labels, this.renderGrid.bind(this)
      this.config.asmtTypes = for asmtType in config.students.customViews.asmtTypes
        asmtType: asmtType.name
        display: asmtType.name

    setFilter: (filter) ->
      this.filter = filter

    sortBySubject: (sort) ->
      this.sort = $.extend(this.sort, sort)
      $('#gridTable').sortBySubject(this.sort.name, this.sort.index, this.sort.order)

    reload: (@param) ->
      # initialize variables
      this.reportType = this.getReportType(param)
      # set current query assessment type
      param.asmtType = this.updateAsmtTypePreference()
      self = this

      this.fetchData param, (data)->
        self.data = data
        self.populationData = self.data.records
        if not self.data.context.items[0]
          # no results
          self.displayNoResults()
          return
        self.summaryData = self.data.summary
        self.asmtSubjectsData = self.data.subjects
        self.notStatedData = self.data.not_stated
        #Check for colors, set to default color if it's null
        for subject, value of self.data.metadata
          if value is null
            self.data.metadata[subject] = self.defaultColors

        # process breadcrumbs
        self.renderBreadcrumbs(self.data.context)
        self.renderReportInfo()
        self.renderReportActionBar()
        self.stickyCompare.setReportInfo self.reportType, self.breadcrumbs.getDisplayType(), self.param
        self.createGrid()
        self.updateDropdown()
        self.updateFilter()
        self.createHeaderAndFooter()
        # Set asmt Subject
        subjects = []
        for key, value of self.asmtSubjectsData
          subjects.push value
        edwarePreferences.saveSubjectPreference subjects

    displayNoResults: () ->
      # no results
      $('#gridTable').jqGrid('GridUnload')
      edwareUtil.displayErrorMessage  this.labels['no_results']

    updateAsmtTypePreference: () ->
      if this.reportType in ['state', 'district']
        # Reset back to summative
        edwarePreferences.saveAsmtPreference Constants.ASMT_TYPE.SUMMATIVE
      # Use this assessment type for school view
      edwarePreferences.getAsmtPreference().toUpperCase()

    updateFilter: ()->
      this.filter.update this.notStatedData

    createHeaderAndFooter: ()->
      this.header = edwareHeader.create(this.data, this.config, "comparing_populations_" + this.reportType) unless this.header

    fetchData: (params, callback)->
      # Determine if the report is state, district or school view"
      options =
        method: "POST"
        params: params

      studentsData = undefined
      edwareDataProxy.getDatafromSource "/data/comparing_populations", options, callback

    # Based on query parameters, return the type of report that the user is requesting for
    getReportType: (params) ->
      if params['schoolGuid']
        reportType = 'school'
      else if params['districtGuid']
        reportType = 'district'
      else if params['stateCode']
        reportType = 'state'
      $('body').addClass reportType
      reportType

    createGrid: () ->
      # Append colors to records and summary section
      # Do not format data, or get breadcrumbs if the result is empty
      preprocessor = new DataProcessor(this.summaryData[0], this.asmtSubjectsData, this.data.metadata, this.defaultColors)
      this.populationData = preprocessor.process(this.populationData)
      summaryData = preprocessor.process(this.summaryData)
      this.summaryData = this.formatSummaryData summaryData
      this.renderGrid()

    afterGridLoadComplete: () ->
      this.bindEvents()
      # Rebind events and reset sticky comparison
      this.stickyCompare.update()
      this.alignment.update()
      # Save the current sorting column and order to apply after filtering
      this.sort = $.extend this.sort, {
        order: $('#gridTable').getGridParam('sortorder')
        name: $('#gridTable').getGridParam('sortname')
      }

    renderGrid: () ->
      $('#gridTable').jqGrid('GridUnload')
      # Change the column name and link url based on the type of report the user is querying for
      this.gridConfig = new ConfigBuilder(this.configTemplate, this.asmtSubjectsData)
                             .customize(this.customViews[this.reportType])
                             .build()

      # Filter out selected rows, if any, we pass in the first columns' grid config field name for sticky chain list
      filteredInfo = this.stickyCompare.getFilteredInfo this.populationData, this.gridConfig[0]["items"][0]["field"]

      self = this

      # Create compare population grid for State/District/School view
      edwareGrid.create {
        data: filteredInfo.data
        columns: this.gridConfig
        footer: this.summaryData
        options:
          gridHeight: this.gridHeight
          labels: this.labels
          stickyCompareEnabled: filteredInfo.enabled
          sort: this.sort
          gridComplete: () ->
            self.afterGridLoadComplete()
      }

    renderBreadcrumbs: (breadcrumbsData)->
      this.breadcrumbs = new Breadcrumbs(breadcrumbsData, this.breadcrumbsConfigs, this.reportType)

    renderReportInfo: () ->
      edwareReportInfoBar.create '#infoBar',
        reportTitle: @breadcrumbs.getReportTitle()
        reportName: Constants.REPORT_NAME.CPOP
        reportInfoText: @config.reportInfo
        labels: @labels
        CSVOptions: @config.CSVOptions

    renderReportActionBar: () ->
      self = this
      @config.colorsData = @data.metadata
      @config.reportName = Constants.REPORT_NAME.CPOP
      @actionBar ?= edwareReportActionBar.create '#actionBar', @config, () ->
        self.reload self.param

    bindEvents: ()->
      # Show tooltip for population bar on mouseover
      $(".progress").popover
            html: true
            placement: 'top'
            container: '#content'
            trigger: 'hover'
            content: ->
              $(this).find(".progressBar_tooltip").html() # template location: widgets/populatoinBar/template.html

      self = this
      $('#gridTable_name').click ->
        # Get the current sort column and reset cpop sorting dropdown if the current sort column is the first column
        self.edwareDropdown.resetAll()

    updateDropdown: ()->
      # create drop down menus
      @edwareDropdown ?= this.createDropdown(this.config.comparingPopulations.customALDDropdown)
      # update dropdown menus status
      this.edwareDropdown.update(this.summaryData, this.asmtSubjectsData, this.data.metadata)

    createDropdown: (customALDDropdown)->
      self = this
      $('.dropdownSection').edwareDropdown customALDDropdown, (subject, index)->
        self.sortBySubject subject, index

      # Format the summary data for summary row rendering purposes
    formatSummaryData: (summaryData) ->
      summaryRowName = this.breadcrumbs.getOverallSummaryName()
      data = {}
      summaryData = summaryData[0]
      for k of summaryData.results
        name = 'results.' + k + '.total'
        data[name] = summaryData.results[k].total

      data['subtitle'] = this.labels['reference_point']#'Reference Point'
      # Set header row to be true to indicate that it's the summary row
      data['header'] = true
      data['results'] = summaryData.results
      data['name'] = summaryRowName
      data


  class Breadcrumbs

    constructor: (@breadcrumbsData, @breadcrumbsConfigs, @reportType) ->
      # Render breadcrumbs on the page
      $('#breadcrumb').breadcrumbs(breadcrumbsData, breadcrumbsConfigs)
      this.initialize()

    initialize: () ->
      if this.reportType is 'state'
        this.orgType = this.breadcrumbsData.items[0].name
        this.displayType = "District"
      else if this.reportType is 'district'
        this.orgType = this.breadcrumbsData.items[1].name
        this.displayType = "School"
      else if this.reportType is 'school'
        this.orgType = this.breadcrumbsData.items[2].name
        this.displayType = "Grade"

    getOrgType: () ->
      this.orgType

    getDisplayType: () ->
      this.displayType

    getReportTitle: () ->
    # Returns report title based on the type of report
      'Comparing '+ this.addApostropheS(this.orgType) + ' ' + this.displayType + 's' + ' on Math & ELA'

    # Format the summary data for summary row purposes
    getOverallSummaryName: () ->
        # Returns the overall summary row name based on the type of report
      if this.reportType is 'state'
        return this.breadcrumbsData.items[0].id + ' State Overall'
      else if this.reportType is 'district'
        districtName = this.breadcrumbsData.items[1].name
        districtName = $.trim districtName.replace(/(Schools)|(Public Schools)$/, '')
        districtName = $.trim districtName.replace(/District$/, '')
        districtName = $.trim districtName.replace(/School$/, '')
        return districtName + ' District Overall'
      else if this.reportType is 'school'
        schoolName = this.breadcrumbsData.items[2].name
        schoolName = $.trim schoolName.replace(/School$/, '')
        return schoolName + ' School Overall'
      else
        return this.breadcrumbsData.items[3].name + ' Overall'

    # Add an 's to a word
    addApostropheS: (word) ->
      if word.substr(word.length - 1) is "s"
        word = word + "'"
      else
        word = word + "'s"
      word


  class DataProcessor

    constructor: (@summaryData, @asmtSubjectsData, @colorsData, @defaultColors) ->

    # Traverse through to intervals to prepare to append color to data
    # Handle population bar alignment calculations
    process: (data) ->
      data = this.appendColors data
      data = this.appendAlignmentOffset data
      data = this.appendSortingAccessor data
      data

    appendColors: (data) ->
      for item in data
        for subject of this.asmtSubjectsData
          subjectData = item['results'][subject]
          if subjectData
            this.appendColor subjectData, this.colorsData[subject]
      data

    appendAlignmentOffset: (data) ->
      for item in data
        for subject of this.asmtSubjectsData
          subjectData = item['results'][subject]
          summary = this.summaryData.results[subject]
          if summary and subjectData
            summaryDataAlignment = summary.intervals[0].percentage + summary.intervals[1].percentage
            subjectData.alignmentLine =  (((summaryDataAlignment) * POPULATION_BAR_WIDTH) / 100) + 10 + 35
            subjectData.alignment =  (((summaryDataAlignment - 100 + subjectData.sort[1]) * POPULATION_BAR_WIDTH) / 100) + 10
      data

    appendSortingAccessor: (data) ->
      for item in data
        for subject of this.asmtSubjectsData
          subjectData = item['results'][subject]
          if subjectData
            item[subjectData.asmt_subject] = subjectData.sort
      data

      # Add color for each intervals
    appendColor: (data, colors) ->
      i = 0
      defaultColors = this.defaultColors
      intervals = data.intervals
      len = colors['colors'].length
      sort = prepareTotalPercentage data.total, len
      while i < len
        element = intervals[i]
        element = {'count': 0, 'percentage': 0} if element is undefined
        if colors and colors[i]
          element.color = colors[i]
        else
          element.color = defaultColors[i]

        # if percentage is less than 9 then remove the percentage text from the bar
        if element.percentage > 9
          element.showPercentage = true
        else
          element.showPercentage = false

        # calculate sort
        sort = calculateTotalPercentage sort, i, element.percentage
        i++
      # attach sort to data
      data.sort = sort

    # calculate percentages for each sort interval
    calculateTotalPercentage = (percentages, i, currentPercentage) ->
      k = 2
      if i is 0
        percentages[i] = currentPercentage
      else
        while k <= i
          percentages[k-1] = percentages[k-1] + currentPercentage
          k++
      percentages

    # initialize total percentages for each sort interval
    prepareTotalPercentage = (total, intervalLength) ->
      percentages = {}
      j = 0
      while j < intervalLength - 1
        # Prepopulate
        percentages[j] = 0
        j++
      percentages[intervalLength-1] = total
      percentages


  class Alignment

    constructor: (@triggerClass, @labels)->
      this.aligned = false
      this.bindEvents()

    bindEvents: ()->
      # Set population bar alignment on/off
      self = this
      $(document).on 'click', this.triggerClass, () ->
        $alignButton = $(self.triggerClass)
        self.aligned = not self.aligned
        alignText = if self.aligned then self.labels.on else self.labels.off
        # toggle component
        $alignButton.toggleClass('align_on align_off')
        $alignButton.find('span.alignText').text alignText
        # update alignment
        self.update()

    update: () ->
      if this.aligned
        this.showAlignment()
      else
        this.hideAlignment()

    # Change population bar width as per alignment on/off status
    showAlignment: () ->
      $(".barContainer").addClass('alignment').removeClass('default')
      # have to set offset for alignment line manually because IE doesn't contain those information for some reason
      $(".alignmentLine").each ()->
        $this = $(this)
        $this.css "margin-left", $this.data('alignment-offset')
      # update population bar offset
      $(".populationBar").each ()->
        $this = $(this)
        $this.css "margin-left", $this.data('margin-left')

    hideAlignment: () ->
      $(".barContainer").addClass('default').removeClass('alignment')
      $(".populationBar").removeAttr('style')


  PopulationGrid: PopulationGrid
