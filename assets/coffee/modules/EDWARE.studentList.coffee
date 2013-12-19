#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareGrid"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareHeader"
  "edwarePreferences"
  "edwareConstants"
  "edwareGridStickyCompare"
  "edwareReportInfoBar"
  "edwareReportActionBar"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences,  Constants, edwareStickyCompare, edwareReportInfoBar, edwareReportActionBar) ->

  LOS_HEADER_BAR_TEMPLATE = $('#edwareLOSHeaderConfidenceLevelBarTemplate').html()

  class StudentGrid

    constructor: () ->
      configPromise = edwareDataProxy.getDataForReport Constants.REPORT_JSON_NAME.LOS
      configPromise.done @initialize.bind(@)

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
      this.gridHeight = window.innerHeight - 212
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
        # append cutpoints into each individual assessment data
        self.formatAssessmentsData self.cutPointsData
        self.stickyCompare.setReportInfo Constants.REPORT_JSON_NAME.LOS, "student", params
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
      self = this
      @config.colorsData = @cutPointsData
      @config.reportName = Constants.REPORT_NAME.LOS
      asmtTypeDropdown = convertAsmtTypes this.studentsConfig.customViews, this.subjectsData
      @config.asmtTypes = asmtTypeDropdown
      @actionBar ?= edwareReportActionBar.create '#actionBar', @config, (viewName) ->
        # Add dark border color between Math and ELA section to emphasize the division
        $('#gridWrapper').removeClass().addClass(viewName)
        self.updateView viewName

    createGrid: () ->
      # Get asmtType from storage
      defaultView = this.data.subjects.subject1 + "_" + this.data.subjects.subject2
      this.updateView defaultView
      # Set asmt Subject
      subjects = []
      for key, value of this.data.subjects
        subjects.push value
      edwarePreferences.saveSubjectPreference subjects

    updateView: (viewName) ->
      # Save asmtType and viewName
      asmtType = edwarePreferences.getAsmtPreference()
      this.viewName = viewName
      this.renderGrid asmtType, viewName
   
    reloadCurrentView: () ->
      # this is the callback function for sticky compare to reload current view
      this.updateView this.viewName

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
        this.cache[asmtType] ?= {}
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
      combinedData = $.extend(true, {}, this.data.subjects)
      combinedData.claims = claimsData
      columnData = JSON.parse(Mustache.render(JSON.stringify(this.studentsConfig), combinedData))
      columnData

    createDisclaimer: () ->
      this.disclaimer = $('.disclaimerInfo').edwareDisclaimer this.config.interimDisclaimer

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

  convertAsmtTypes = (customViews, subjects) ->
    items = []
    copiedSubjects = jQuery.extend(true, {}, subjects);
    # render dropdown
    for asmtType in customViews.asmtTypes
      copiedSubjects['asmtType'] = asmtType['display']
      for key, value of customViews.items
        items.push {
          'value': Mustache.to_html(key, copiedSubjects)
          'asmtType': asmtType['name']
          'display': Mustache.to_html(value, copiedSubjects)
        }
    items

  StudentGrid: StudentGrid
