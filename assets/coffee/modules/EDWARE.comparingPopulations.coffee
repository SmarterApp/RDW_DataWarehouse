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
  "edwareGridStickyCompare"
  "edwarePreferences"
  "edwareConstants"
  "edwareClientStorage"
  "edwareReportInfoBar"
  "edwareReportActionBar"
  "edwareContextSecurity"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareHeader, edwareStickyCompare, edwarePreferences, Constants, edwareClientStorage, edwareReportInfoBar, edwareReportActionBar, contextSecurity) ->

  POPULATION_BAR_WIDTH = 145

  class ConfigBuilder

    constructor: (template, subjects) ->
      output = Mustache.render(JSON.stringify(template), subjects)
      this.gridConfig = JSON.parse(output)
      this

    customize: (customView) ->
      firstColumn = this.gridConfig[0].items[0]
      firstColumn.name = customView.name
      firstColumn.displayTpl = customView.displayTpl
      firstColumn.exportName = customView.exportName
      firstColumn.options.linkUrl = customView.link
      firstColumn.options.id_name = customView.id_name
      firstColumn.sorttype = "int" if customView.name is "Grade"
      this

    build: ()->
      this.gridConfig


  class PopulationGrid

    constructor: (config) ->
      @initialize(config)

    initialize: (config)->
      this.config = config
      this.breadcrumbsConfigs = config.breadcrumb
      this.configTemplate = config.comparingPopulations.grid
      this.customViews = config.comparingPopulations.customViews
      this.labels = config.labels
      this.defaultColors = config.colors
      this.gridContainer = $('.gridHeight100')
      # create align button
      this.alignment = new Alignment('.align_button', @labels)
      # default sort
      this.sort = {
        name: 'name'
        order: 'asc'
      }
      self = this
      this.stickyCompare = new edwareStickyCompare.EdwareGridStickyCompare this.labels, ()->
        self.renderGrid()

    setFilter: (filter) ->
      this.filter = filter

    reload: (@param) ->
      # initialize variables
      this.reportType = this.getReportType(param)
      self = this

      loadingData = this.fetchData param
      loadingData.done (data)->
        self.data = data
        self.populationData = self.data.records
        if self.populationData.length is 0
          # no results
          self.displayNoResults()
          return
        self.summaryData = self.data.summary
        self.asmtSubjectsData = self.data.subjects
        self.academicYears = self.data.asmt_period_year
        self.notStatedData = self.data.not_stated
        #Check for colors, set to default color if it's null
        for subject, value of self.data.metadata
          if value is null
            self.data.metadata[subject] = self.defaultColors

        # initialize context security
        contextSecurity.init data.context.permissions, self.config

        # process breadcrumbs
        self.renderBreadcrumbs(self.data.context, self.labels)
        self.renderReportInfo()
        self.renderReportActionBar()
        self.stickyCompare.setReportInfo self.reportType, self.breadcrumbs.getDisplayType(), self.param
        self.createHeaderAndFooter()
        self.createGrid()
        self.updateFilter()
        # Set asmt Subject
        subjects = []
        for key, value of self.asmtSubjectsData
          subjects.push value
        edwarePreferences.saveSubjectPreference subjects

    displayNoResults: () ->
      # no results
      $('#gridTable').jqGrid('GridUnload')
      edwareUtil.displayErrorMessage  this.labels['no_results']

    updateFilter: ()->
      this.filter.update this.notStatedData

    createHeaderAndFooter: ()->
      self = this
      this.header ?= edwareHeader.create this.data, this.config

    fetchData: (params)->
      options =
        method: "POST"
        params: params

      edwareDataProxy.getDatafromSource "/data/comparing_populations", options

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
      # TODO: need to get cut_point_intervals from database
      preprocessor = new DataProcessor(@summaryData[0], @asmtSubjectsData, @data.metadata, @defaultColors, @config.legendInfo.sample_intervals.cut_point_intervals)
      this.populationData = preprocessor.process(this.populationData)
      summaryData = preprocessor.process(this.summaryData)
      this.summaryData = this.formatSummaryData summaryData
      this.renderGrid()

    afterGridLoadComplete: () ->
      this.bindEvents()
      # Rebind events and reset sticky comparison
      this.stickyCompare.update()
      this.alignment.update()
      this.actionBar.update()
      # Save the current sorting column and order to apply after filtering
      name = $('#gridTable').getGridParam('sortname')
      order = $('#gridTable').getGridParam('sortorder')
      this.sort = $.extend this.sort, {
        order: order
        name: name
      }
      # We need to preserve sorting, so, update the column labels and color
      this.updateSortLabels(name, order)
      # apply context security
      contextSecurity.apply()

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
      @grid = edwareGrid.create {
        data: filteredInfo.data
        columns: this.gridConfig
        footer: this.summaryData
        options:
          labels: this.labels
          stickyCompareEnabled: filteredInfo.enabled
          sort: this.sort
          gridComplete: () ->
            self.afterGridLoadComplete()
      }
      $(document).trigger Constants.EVENTS.SORT_COLUMNS

    updateSortLabels: (index, sortorder) ->
      # Remove second row header as that counts as a column in setLabel function
      $('.jqg-second-row-header').remove()
      grid = $('#gridTable')
      colModels = grid.jqGrid('getGridParam').colModel
      # Reset back to original color for all columns
      for colModel in colModels
        #reset labels
        label = "<a class='inherit' href='#'>#{colModel.label}</a>"
        grid.jqGrid('setLabel', colModel.label, label)
        if colModel.name is index
          newLabel = label

      if index in ["results.subject2.sortedValue", "results.subject1.sortedValue"]
        if sortorder is 'asc'
          newLabel = "#{newLabel} <span aria-hidden='true'>#{this.config.proficiencyAscending}</span>"
        else
          newLabel = "#{newLabel} <span aria-hidden='true'>#{this.config.proficiencyDescending}</span>"
      # Set label for active sort column
      grid.jqGrid('setLabel', index, newLabel, '')

      # TODO: need refactoring:
      # get last focused element from EdwareGrid object
      @grid?.resetFocus()

    renderBreadcrumbs: (breadcrumbsData, labels)->
      displayHome = edwareUtil.getDisplayBreadcrumbsHome this.data.user_info
      this.breadcrumbs ?= new Breadcrumbs(breadcrumbsData, this.breadcrumbsConfigs, this.reportType, displayHome, labels)

    renderReportInfo: () ->
      edwareReportInfoBar.create '#infoBar',
        reportTitle: @breadcrumbs.getReportTitle()
        reportName: Constants.REPORT_NAME.CPOP
        reportInfoText: @config.reportInfo
        labels: @labels
        CSVOptions: @config.CSVOptions
        ExportOptions: @config.ExportOptions
        param: @param
        academicYears:
          options: @academicYears
          callback: @onAcademicYearSelected.bind(this)
        getReportParams: @getReportParams.bind(this)

    getReportParams: () ->
      grades = for data in @populationData
        data.id
      # backend expects asmt grades as a list
      params = {}
      params["asmtGrade"] = grades if grades.length isnt 0
      params


    renderReportActionBar: () ->
      self = this
      @config.colorsData = @data.metadata
      @config.reportName = Constants.REPORT_NAME.CPOP
      # placeholder text for search box
      @config.labels.searchPlaceholder = @config.searchPlaceholder[@reportType]
      @config.labels.SearchResultText = @config.SearchResultText
      @actionBar ?= edwareReportActionBar.create '#actionBar', @config, () ->
        self.reload self.param

    onAcademicYearSelected: (year) ->
      @param['asmtYear'] = year
      @reload @param

    bindEvents: ()->
      # Show tooltip for population bar on mouseover
      $(".progress").popover
            html: true
            placement: 'top'
            container: '#content'
            trigger: 'hover'
            content: ->
              # template location: widgets/populationBar/template.html
              $(this).find(".progressBar_tooltip").html()
        # also display tooltips when focus on
      $(".progress").on 'focus', ()->
        $(this).popover('show')
      .focusout ()->
        $(this).popover('hide')

    # Format the summary data for summary row rendering purposes
    formatSummaryData: (summaryData) ->
      summaryRowName = this.breadcrumbs.getOverallSummaryName()
      data = {}
      summaryData = summaryData[0]
      for k of summaryData.results
        name = 'results.' + k + '.total'
        data[name] = summaryData.results[k].total
        # Note that this name must be the same as index/field in jqgrid config
        name = 'results.' + k + '.sortedValue'
        data[name] = summaryData.results[k].sortedValue

      data['subtitle'] = this.labels['reference_point']#'Reference Point'
      # Set header row to be true to indicate that it's the summary row
      data['header'] = true
      data['results'] = summaryData.results
      data['name'] = summaryRowName
      data


  class Breadcrumbs

    constructor: (@breadcrumbsData, @breadcrumbsConfigs, @reportType, @displayHome, @labels) ->
      # Render breadcrumbs on the page
      $('#breadcrumb').breadcrumbs(breadcrumbsData, breadcrumbsConfigs, @displayHome, @labels)
      this.initialize()

    initialize: () ->
      if this.reportType is 'state'
        this.orgType = this.breadcrumbsData.items[1].name
        this.displayType = "District"
        this.title = 'Comparing ' + this.displayType + 's in ' + this.orgType + ' on Math & ELA'
      else if this.reportType is 'district'
        this.orgType = this.breadcrumbsData.items[2].name
        this.displayType = "School"
        this.title = 'Comparing ' + this.displayType + 's in ' + this.orgType + ' on Math & ELA'
      else if this.reportType is 'school'
        this.orgType = this.breadcrumbsData.items[3].name
        this.displayType = "Grade"
        this.title = 'Results by Grade for ' + this.orgType + ' on Math & ELA'

    getDisplayType: () ->
      this.displayType

    getReportTitle: () ->
    # Returns report title based on the type of report
      this.title

    # Format the summary data for summary row purposes
    getOverallSummaryName: () ->
        # Returns the overall summary row name based on the type of report
      if this.reportType is 'state'
        return this.breadcrumbsData.items[1].id + ' State Overall'
      else if this.reportType is 'district'
        districtName = this.breadcrumbsData.items[2].name
        districtName = $.trim districtName.replace(/(Schools)|(Public Schools)$/, '')
        districtName = $.trim districtName.replace(/District$/, '')
        districtName = $.trim districtName.replace(/School$/, '')
        return districtName + ' District Overall'
      else if this.reportType is 'school'
        schoolName = this.breadcrumbsData.items[3].name
        schoolName = $.trim schoolName.replace(/School$/, '')
        return schoolName + ' School Overall'
      else
        return this.breadcrumbsData.items[4].name + ' Overall'

    # Add an 's to a word
    addApostropheS: (word) ->
      if word.substr(word.length - 1) is "s"
        word = word + "'"
      else
        word = word + "'s"
      word


  class DataProcessor

    constructor: (@summaryData, @asmtSubjectsData, @colorsData, @defaultColors, @intervals) ->

    # Traverse through to intervals to prepare to append color to data
    # Handle population bar alignment calculations
    process: (data) ->
      data = this.processDataForSubject data
      data = this.appendAlignmentOffset data
      data

    processDataForSubject: (data) ->
      for subject of this.asmtSubjectsData
        interimCount = 0
        for item in data
          subjectData = item['results'][subject]
          if subjectData
            this.appendColor subjectData, this.colorsData[subject]
            if subjectData['hasInterim']
              interimCount += 1
        # Summary row hasInterim when one of the rows is an Interim row and Summary row has no data
        this.summaryData['results'][subject]['hasInterim'] = (interimCount > 0 and this.summaryData['results'][subject]['total'] is 0)
      data

    appendAlignmentOffset: (data) ->
      for item in data
        for subject of this.asmtSubjectsData
          subjectData = item['results'][subject]
          summary = this.summaryData.results[subject]
          if summary and subjectData
            summaryDataAlignment = summary.intervals[0].percentage + summary.intervals[1].percentage
            subjectData.alignmentLine =  (((summaryDataAlignment) * POPULATION_BAR_WIDTH) / 100) + 10 + 35
            subjectData.alignment =  (((summaryDataAlignment - 100 + subjectData.sortedValue) * POPULATION_BAR_WIDTH) / 100) + 10
      data

      # Add color for each intervals
    appendColor: (data, colors) ->
      i = 0
      defaultColors = this.defaultColors
      intervals = data.intervals
      if colors and colors['colors'] then len = colors['colors'].length else len = defaultColors.length
      sort = 0
      while i < len and intervals
        element = intervals[i]
        element = {'count': 0, 'percentage': 0} if element is undefined
        element.count = edwareUtil.formatNumber(element.count)
        element.description = @intervals[i].name
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
        if i >= intervals.length/2
          sort += element.percentage
        i++
      # attach sort to data
      data.sortedValue = sort
      # reformat
      if data.unfilteredTotal
        ratio = data.total * 100.0 / data.unfilteredTotal
        data.ratio = edwareUtil.formatNumber(Math.round(ratio))
        data.unfilteredTotal = edwareUtil.formatNumber(data.unfilteredTotal)
      data.total = edwareUtil.formatNumber(data.total)

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
