#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareGrid"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareFooter"
  "edwareHeader"
  "edwarePreferences"
  "edwareConstants"
  "edwareGridStickyCompare"
  "edwareReportInfoBar"
  "edwareReportActionBar"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareFooter, edwareHeader, edwarePreferences,  Constants, edwareStickyCompare, edwareReportInfoBar, edwareReportActionBar) ->

  REPORT_NAME = 'studentList'

  DROPDOWN_VIEW_TEMPLATE = $('#assessmentDropdownViewTemplate').html()

  LOS_HEADER_BAR_TEMPLATE = $('#edwareLOSHeaderConfidenceLevelBarTemplate').html()

  class StudentGrid

    constructor: () ->
      config = edwareDataProxy.getDataForReport REPORT_NAME
      this.initialize(config)

    initialize: (config) ->
      this.config = config
      this.defaultColors = config.colors
      this.feedbackData = config.feedback
      this.breadcrumbsConfigs = config.breadcrumb
      this.reportInfo = config.reportInfo
      this.studentsConfig = config.students
      this.asmtTypes = config.students.customViews.asmtTypes
      this.legendInfo = config.legendInfo
      this.labels = config.labels
      this.gridHeight = window.innerHeight - 235
      edwareUtil.reRenderBody this.labels
      this.stickyCompare = new edwareStickyCompare.EdwareGridStickyCompare this.labels, this.reloadCurrentView.bind(this)

    reload: (params) ->
      self = this
      this.fetchData params, (data)->
        self.data = data
        self.assessmentsData = data.assessments
        self.contextData = data.context
        self.subjectsData = data.subjects
        self.userData = data.user_info
        self.cutPointsData = self.createCutPoints()
        self.columnData = self.createColumns()
        #  append cutpoints into each individual assessment data
        self.formatAssessmentsData self.cutPointsData
        self.stickyCompare.setReportInfo REPORT_NAME, "student", params
        # process breadcrumbs
        self.renderBreadcrumbs(data.context)
        self.renderReportInfo()
        self.renderReportActionBar()
        self.createHeaderAndFooter()
        self.createGrid()
        self.bindEvents()

    createCutPoints: () ->
      cutPointsData = this.data.metadata.cutpoints
      cutPointsData = JSON.parse(Mustache.render(JSON.stringify(cutPointsData),this.data))
      #if cut points don't have background colors, then it will use default background colors
      for key, items of cutPointsData
        for interval, i in items.cut_point_intervals
          if not interval.bg_color
            $.extend(interval, this.defaultColors[i])
      cutPointsData

    bindEvents: ()->
      # Show tooltip for overall score on mouseover
      $(document).on
        mouseenter: ->
          elem = $(this)
          elem.popover
            html: true
            trigger: "manual"
            container: '#content'
            placement: (tip, element) ->
              edwareUtil.popupPlacement(element, 400, 220)
            title: ->
              elem.parent().find(".losTooltip .js-popupTitle").html()
            template: '<div class="popover losPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
            content: ->
              elem.parent().find(".losTooltip").html() # html is located in widgets/EDWARE.grid.formatter performanceBar method
          .popover("show")
        click: (e) ->
          e.preventDefault()
        mouseleave: ->
          elem = $(this)
          elem.popover("hide")
      , ".asmtScore"

    createHeaderAndFooter: () ->
      this.footer = new edwareFooter.EdwareFooter(Constants.REPORT_NAME.LOS, this.config, this.fetchExportData.bind(this)) unless this.footer
      this.header = edwareHeader.create(this.data, this.config, 'list_of_students') unless this.header

    fetchExportData: () ->
      this.assessmentsData

    renderBreadcrumbs: () ->
      $('#breadcrumb').breadcrumbs(this.contextData, this.breadcrumbsConfigs)

    renderReportInfo: () ->
      edwareReportInfoBar.create '#infoBar',
        reportTitle: @contextData.items[2].name # set school name as the page title from breadcrumb
        reportName: Constants.REPORT_NAME.LOS
        reportInfoText: @config.reportInfo
        labels: @labels
        CSVOptions: @config.CSVOptions

    renderReportActionBar: () ->
      @config.colorsData = @cutPointsData
      @config.reportName = Constants.REPORT_NAME.LOS
      @config.asmtTypes = @subjectsData
      #this.asmtTypeDropdown = new AsmtTypeDropdown this.studentsConfig.customViews, this.subjectsData, this.updateView.bind(this)
      @actionBar ?= edwareReportActionBar.create '#actionBar', @config, @reloadCurrentView.bind(this)

    createGrid: () ->
      # populate select view, only create the dropdown when it doesn't exit
      # TODO this.createDropdown() if not this.asmtTypeDropdown
      # TODO this.createDisclaimer() if not this.disclaimer
      # Get asmtType from storage
      this.asmtType = edwarePreferences.getAsmtPreference() || 'Summative'
      this.currentView = this.data.subjects.subject1 + "_" + this.data.subjects.subject2
      this.updateView this.asmtType, this.currentView

    updateView: (asmtType, viewName) ->
      # Save asmtType and viewName
      this.asmtType = asmtType
      this.viewName = viewName
      # set dropdown text
      this.asmtTypeDropdown.setSelectedText asmtType, viewName
      # save preference to storage
      edwarePreferences.saveAsmtPreference asmtType
      this.renderGrid asmtType, viewName
      # show the content upon rendering complete to prevent seeing the pre-templated text on the html
      $('.gridControls').show()
      this.updateDisclaimer asmtType
   
    reloadCurrentView: () ->
      # this is the callback function for sticky compare to reload current view
      this.updateView this.asmtType, this.viewName

    fetchData: (params, callback) ->
      # Determine if the report is state, district or school view"
      options =
        method: "POST"
        params: params

      studentsData = undefined
      labels = this.labels
      edwareDataProxy.getDatafromSource "/data/list_of_students", options, (data)->
        studentsData = JSON.parse(Mustache.render(JSON.stringify(data), {"labels": labels}))
        callback studentsData

    # For each subject, filter out its data
    # Also append cutpoints & colors into each assessment
    formatAssessmentsData: (assessmentCutpoints) ->
      this.cache = {}
      allSubjects = this.data.subjects.subject1 + "_" + this.data.subjects.subject2
      for asmt in this.asmtTypes
        asmtType = asmt['name']
        this.cache[asmtType] = {} if not this.cache[asmtType]
        this.cache[asmtType][allSubjects] = [] if not this.cache[asmtType][allSubjects]
        for row in this.assessmentsData
          # Format student name
          row['student_full_name'] = edwareUtil.format_full_name_reverse row['student_first_name'], row['student_middle_name'], row['student_last_name']
          # This is for links in drill down
          row['params'] = {"studentGuid": row['student_guid']}
          assessment = row[asmtType]
          this.cache[asmtType][allSubjects].push row if assessment
          for key, value of this.subjectsData
            # check that we have such assessment first, since a student may not have taken it
            if assessment and key of assessment
              cutpoint = assessmentCutpoints[key]
              $.extend assessment[key], cutpoint
              assessment[key].asmt_type = value # display asssessment type in the tooltip title
              if assessment[key].asmt_perf_lvl > assessment[key].cut_point_intervals.length # this is to prevent bad data where there is no color an asmt_perf_lvl that is out of range
                assessment[key].score_bg_color = "#D0D0D0"
                assessment[key].score_text_color = "#000000"
              else
                assessment[key].score_bg_color = assessment[key].cut_point_intervals[assessment[key].asmt_perf_lvl - 1].bg_color
                assessment[key].score_text_color = assessment[key].cut_point_intervals[assessment[key].asmt_perf_lvl - 1].text_color
              # save the assessment to the particular subject
              this.cache[asmtType][value] = [] if not this.cache[asmtType][value]
              this.cache[asmtType][value].push row

    afterGridLoadComplete: () ->
      this.stickyCompare.update()

    renderGrid: (asmtType, viewName) ->
      $('#gridTable').jqGrid('GridUnload')
      # get filtered data and we pass in the first columns' grid config field name for sticky chain list
      filteredInfo = this.stickyCompare.getFilteredInfo(this.getAsmtData(asmtType, viewName), this.columnData[viewName][0]["items"][0]["field"])

      self = this
      edwareGrid.create {
        data: filteredInfo.data
        columns: this.columnData[viewName]
        options:
          gridHeight: this.gridHeight
          labels: this.labels
          stickyCompareEnabled: filteredInfo.enabled
          gridComplete: () ->
            self.afterGridLoadComplete()
      }
      #TODO Add dark border color between Math and ELA section to emphasize the division
      $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(1), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(2)').css("border-right", "solid 1px #B1B1B1")
      $('.jqg-second-row-header th:nth-child(3), .jqg-second-row-header th:nth-child(3), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(3), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "none")
      this.renderHeaderPerfBar(this.cutPointsData)

    getAsmtData: (asmtType, viewName)->
      data = this.cache[asmtType][viewName]
      if data
        for item in data
          item.assessments = item[asmtType]
      data

    createColumns: () ->
      # Use mustache template to replace text in json config
      # Add assessments data there so we can get column names
      claimsData = JSON.parse(Mustache.render(JSON.stringify(this.data.metadata.claims), this.data))
      combinedData = this.data.subjects
      combinedData.claims =  claimsData
      columnData = JSON.parse(Mustache.render(JSON.stringify(this.studentsConfig), combinedData))
      columnData

    # creating the assessment view drop down
    createDropdown: ()->
      this.asmtTypeDropdown = new AsmtTypeDropdown this.studentsConfig.customViews, this.subjectsData, this.updateView.bind(this)

    createDisclaimer: () ->
      this.disclaimer = $('.disclaimerInfo').edwareDisclaimer this.config.interimDisclaimer

    updateDisclaimer: (asmtType) ->
      this.disclaimer.update asmtType

    renderHeaderPerfBar: (cutPointsData) ->
      for key of cutPointsData
          items = cutPointsData[key]
          items.bar_width = 120

          items.asmt_score_min = items.asmt_score_min
          items.asmt_score_max = items.asmt_score_max

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
          output = Mustache.to_html LOS_HEADER_BAR_TEMPLATE, items
          $("#"+key+"_perfBar").html(output)

  class AsmtTypeDropdown

    constructor: (customViews, subjects, @callback) ->
      items = []
      # render dropdown
      for asmtType in customViews.asmtTypes
        subjects['asmtType'] = asmtType['display']
        for key, value of customViews.items
          items.push {
            'key': Mustache.to_html(key, subjects)
            'value': Mustache.to_html(value, subjects)
            'asmtType': asmtType['name']
            'id': this.formatAsmt asmtType['name']
          }
      $("#asmtTypeDropdown").html Mustache.to_html DROPDOWN_VIEW_TEMPLATE, {'items': items}
      # bind events
      this.bindEvents()
      # the first element name as default view
      this.currentView = items[0].key
      this.asmtType = items[0].asmtType

    bindEvents: () ->
      self = this
      # add event to change view for assessment
      $(document).on 'click', '.viewOptions', (e) ->
        e.preventDefault()
        viewName = $(this).data('name')
        asmtType = $(this).data('type')
        self.currentView = viewName
        self.asmtType = asmtType
        self.callback asmtType, viewName

        # Add dark border color between Math and ELA section to emphasize the division
        if viewName is "Math_ELA"
          $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(1), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(2)').css("border-right", "solid 1px #b1b1b1")
          $('.jqg-second-row-header th:nth-child(3), .jqg-second-row-header th:nth-child(3), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(3), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "none")
        else
          $('.jqg-second-row-header th:nth-child(1), .jqg-second-row-header th:nth-child(2), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(1), .ui-jqgrid .ui-jqgrid-htable th.ui-th-column:nth-child(2), .ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(2)').css("border-right", "solid 1px #d0d0d0")
          $('.ui-jqgrid tr.jqgrow td:nth-child(1), .ui-jqgrid tr.jqgrow td:nth-child(3)').css("border-right", "solid 1px #E2E2E2")

    getCurrentView: () ->
      this.currentView

    getAsmtType: ()->
      this.asmtType

    formatAsmt: (asmt) ->
      # Replaces spaces with _ for html id purposes
      asmt.replace /\s+/g, "_"

    setSelectedText:(asmtType, view) ->
      name = this.formatAsmt asmtType
      $('#selectedAsmtType').text $('#'+ name + '_' + view).text()

  StudentGrid: StudentGrid
