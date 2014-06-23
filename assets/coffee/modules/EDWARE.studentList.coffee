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
  "edwareContextSecurity"
  "edwareSearch"
  "edwareFilter"
], ($, bootstrap, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences,  Constants, edwareStickyCompare, edwareReportInfoBar, edwareReportActionBar, contextSecurity, edwareSearch, edwareFilter) ->

  LOS_HEADER_BAR_TEMPLATE  = $('#edwareLOSHeaderConfidenceLevelBarTemplate').html()

  EdwareGridStickyCompare = edwareStickyCompare.EdwareGridStickyCompare

  class StudentModel

    constructor: (@effectiveDate, @dataSet) ->

    init: (row) ->
      @appendColors row
      row = @appendExtraInfo row
      row

    appendColors: (assessment) ->
      for key, value of @dataSet.subjectsData
        value = assessment[key]
        continue if not value
        cutpoint = @dataSet.cutPointsData[key]
        $.extend value, cutpoint
        # display asssessment type in the tooltip title
        subjectType = @dataSet.subjectsData[key]
        value.asmt_type = subjectType
        # set default colors for out of range asmt_perf_lvl
        if value.asmt_perf_lvl > value.cut_point_intervals.length
          value.score_bg_color = "#D0D0D0"
          value.score_text_color = "#000000"
        else
          value.score_bg_color = value.cut_point_intervals[value.asmt_perf_lvl - 1].bg_color
          value.score_text_color = value.cut_point_intervals[value.asmt_perf_lvl - 1].text_color

    appendExtraInfo: (row) ->
      # Format student name
      row['student_full_name'] = edwareUtil.format_full_name_reverse row['student_first_name'], row['student_middle_name'], row['student_last_name']
      # This is for links in drill down
      row['params'] = {
        "studentGuid": row['student_guid'],
        "stateCode": row['state_code'],
        "asmtYear": edwarePreferences.getAsmtYearPreference()
      }
      row

  class StudentDataSet

    constructor: (@config) ->
      @asmtTypes = config.students.customViews.asmtTypes

    build: (@data, @cutPointsData, @labels) ->
      @cache = {}
      @allSubjects = "#{data.subjects.subject1}_#{data.subjects.subject2}"
      @assessmentsData  = data.assessments
      @subjectsData = data.subjects
      @columnData = @createColumns()
      @formatAssessmentsData()

    createColumns: () ->
      # Use mustache template to replace text in json config
      # Add assessments data there so we can get column names and translate column names
      claimsData = JSON.parse(Mustache.render(JSON.stringify(this.data.metadata.claims), this.data))
      for idx, claim of claimsData.subject1
        claim.name = @labels.asmt[claim.name]
      for idx, claim of claimsData.subject2
        claim.name = @labels.asmt[claim.name]
      combinedData = $.extend(true, {}, this.data.subjects)
      combinedData.claims = claimsData
      columnData = JSON.parse(Mustache.render(JSON.stringify(@config.students), combinedData))
      columnData

    # For each subject, filter out its data
    # Also append cutpoints & colors into each assessment
    formatAssessmentsData: () ->
      for effectiveDate, assessments of @assessmentsData
        @cache[effectiveDate] ?= {}
        for asmtType, studentList of assessments
          @cache[effectiveDate][asmtType] ?= {}
          for studentId, assessment of studentList
            continue if assessment.hide
            row = new StudentModel(effectiveDate, this).init assessment
            showAllSubjects = false
            # push to each subject view
            for subjectName, subjectType of @subjectsData
              continue if not row[subjectName] or row[subjectName].hide
              @cache[effectiveDate][asmtType][subjectType] ?= []
              @cache[effectiveDate][asmtType][subjectType].push row
              showAllSubjects = true

            continue if not showAllSubjects
            # push to conjunct Math_ELA view
            @cache[effectiveDate][asmtType][@allSubjects] ?= []
            allsubjects = @cache[effectiveDate][asmtType][@allSubjects]
            allsubjects.push row  if row not in allsubjects

    getAsmtData: (viewName)->
      # Saved asmtType and viewName
      asmt = edwarePreferences.getAsmtPreference()
      #TODO asmtGuid = @asmtGuid
      # if not @cache[asmtGuid]
        #reload from server
        # window.location.reload()
      effectiveDate = asmt.effectiveDate
      asmtType = asmt.asmtType
      data = @cache[effectiveDate]?[asmtType]?[viewName]
      if data
        for item in data
          item.assessments = item[asmtType]
      data


  class StudentGrid

    constructor: (@config) ->
      @studentsDataSet = new StudentDataSet(config)
      @reportInfo = config.reportInfo
      @studentsConfig = config.students
      @legendInfo = config.legendInfo
      @labels = config.labels
      self = this
      @stickyCompare ?= new EdwareGridStickyCompare @labels, ()->
        self.updateView()

    reload: (@params)->
      @fetchData params
      @stickyCompare.setReportInfo Constants.REPORT_JSON_NAME.LOS, "student", params

    renderFilter: () ->
      self = this
      edwareDataProxy.getDataForFilter().done (configs)->
        configs = self.mergeFilters(configs)
        filter = $('#losFilter').edwareFilter '.filterItem', configs, self.createGrid.bind(self)
        filter.loadReport()
        filter.update {}

    mergeFilters: (configs) ->
      template = JSON.stringify(configs.group_template)
      for group in @data.groups
        filter = JSON.parse(Mustache.render template, group)
        filter.options = group.options
        configs.filters.push filter
      return configs

    loadPage: (@data) ->
      @cutPointsData = @createCutPoints()
      @contextData = data.context
      @subjectsData = data.subjects
      @userData = data.user_info
      @academicYears = data.asmt_period_year
      @grade = @contextData['items'][4]
      @renderBreadcrumbs(@labels)
      @renderReportInfo()
      @renderReportActionBar()
      @renderFilter()
      @createHeaderAndFooter()

      # @createGrid()
      @bindEvents()
      @applyContextSecurity()

    applyContextSecurity: ()->
      # init context security
      contextSecurity.init @data.context.permissions, @config
      contextSecurity.apply()

    createCutPoints: () ->
      cutPointsData = @data.metadata.cutpoints
      cutPointsData = JSON.parse(Mustache.render(JSON.stringify(cutPointsData),@data))
      #if cut points don't have background colors, then it will use default background colors
      for key, items of cutPointsData
        for interval, i in items.cut_point_intervals
          if not interval.bg_color
            $.extend(interval, @config.colors[i])
      cutPointsData

    bindEvents: ()->
      # Show tooltip for overall score on mouseover
      $(document).on
        'mouseenter focus': ->
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
        'mouseleave focusout': ->
          elem = $(this)
          elem.popover("hide")
      , ".asmtScore"

    createHeaderAndFooter: () ->
      self = this
      this.header = edwareHeader.create(this.data, this.config) unless this.header

    fetchExportData: () ->
      this.assessmentsData

    renderBreadcrumbs: (labels) ->
      displayHome = edwareUtil.getDisplayBreadcrumbsHome this.data.user_info
      $('#breadcrumb').breadcrumbs(@contextData, @config.breadcrumb, displayHome, labels)

    renderReportInfo: () ->
      edwareReportInfoBar.create '#infoBar',
        reportTitle: "Student Results for " + @contextData.items[4].name + " at " + @contextData.items[3].name # set school name as the page title from breadcrumb
        reportName: Constants.REPORT_NAME.LOS
        reportInfoText: @config.reportInfo
        labels: @labels
        CSVOptions: @config.CSVOptions
        ExportOptions: @config.ExportOptions
        academicYears:
          options: @academicYears
          callback: @onAcademicYearSelected.bind(this)
        getReportParams: @getReportParams.bind(this)

    getReportParams: () ->
      params = {}
      studentIDs = @stickyCompare.getRows()
      params["studentGuid"] = studentIDs if studentIDs.length isnt 0
      params

    onAcademicYearSelected: (year) ->
      edwarePreferences.clearAsmtPreference()
      @params['asmtYear'] = year
      @reload @params

    renderReportActionBar: () ->
      self = this
      @config.colorsData = @cutPointsData
      @config.reportName = Constants.REPORT_NAME.LOS
      asmtTypeDropdown = @convertAsmtTypes @data.asmt_administration
      @config.asmtTypes = asmtTypeDropdown
      # placeholder text for search box
      @config.labels.searchPlaceholder = @config.searchPlaceholder
      @config.labels.SearchResultText = @config.SearchResultText
      @actionBar = edwareReportActionBar.create '#actionBar', @config, (asmt) ->
        # save assessment type
        edwarePreferences.saveAsmtPreference asmt
        edwarePreferences.saveAsmtForISR asmt
        self.updateView()

    createGrid: (filters) ->
      data = edwareFilter.filterData(@data, filters)
      @studentsDataSet.build data, @cutPointsData, @labels
      @updateView()
      #TODO: Set asmt Subject
      subjects = []
      for key, value of @data.subjects
        subjects.push value
      edwarePreferences.saveSubjectPreference subjects

    updateView: () ->
      viewName = edwarePreferences.getAsmtPreference().asmtView
      viewName = viewName || @studentsDataSet.allSubjects
      # Add dark border color between Math and ELA section
      $('#gridWrapper').removeClass().addClass(viewName)
      this.renderGrid viewName

    fetchData: (params) ->
      self = this
      loadingData = edwareDataProxy.getDatafromSource "/data/list_of_students",
        method: "POST"
        params: params
      loadingData.done (data)->
        compiled = Mustache.render JSON.stringify(data), "labels": self.labels
        self.loadPage JSON.parse compiled

    afterGridLoadComplete: () ->
      this.stickyCompare.update()
      this.actionBar.update()
      # Remove second row header as that counts as a column in setLabel function
      $('.jqg-second-row-header').remove()

    renderGrid: (viewName) ->
      $('#gridTable').jqGrid('GridUnload')
      asmtData = @studentsDataSet.getAsmtData(viewName)
      filedName = @studentsDataSet.columnData[viewName][0]["items"][0]["field"]
      # get filtered data and we pass in the first columns' config
      # field name for sticky chain list
      filteredInfo = this.stickyCompare.getFilteredInfo(asmtData, filedName)

      self = this
      edwareGrid.create {
        data: filteredInfo.data
        columns: @studentsDataSet.columnData[viewName]
        options:
          labels: this.labels
          stickyCompareEnabled: filteredInfo.enabled
          gridComplete: () ->
            self.afterGridLoadComplete()
      }
      this.renderHeaderPerfBar()
      $(document).trigger Constants.EVENTS.SORT_COLUMNS

    createDisclaimer: () ->
      @disclaimer = $('.disclaimerInfo').edwareDisclaimer @config.interimDisclaimer

    renderHeaderPerfBar: () ->
      cutPointsData = @studentsDataSet.cutPointsData
      for key, items of cutPointsData
        items.bar_width = 120
        score_range = items.asmt_score_max - items.asmt_score_min

        # Calculate width for cutpoints other than first and last cutpoints
        precedence = { interval: items.asmt_score_min }
        for interval in items.cut_point_intervals
          current_span = (interval.interval - precedence.interval)
          interval.asmt_cut_point = items.bar_width * current_span / score_range
          precedence = interval
        # use mustache template to display the json data
        output = Mustache.to_html LOS_HEADER_BAR_TEMPLATE, items
        rainbowAnchor = $("#"+key+"_perfBar")
        rainbowAnchor.html(output)
        rainbowAnchor.closest('th').append(rainbowAnchor)


    convertAsmtTypes: (asmtAdministration) ->
      selectors = []
      for asmt in asmtAdministration
        selector = {}
        # mapping asmt type to capitalized case
        selector.asmt_type = Constants.ASMT_TYPE[asmt.asmt_type]
        selector.effective_date = asmt.effective_date
        selector.asmt_grade = this.grade.name
        selector.display = "{{effectiveDateText}} · {{asmtGrade}} · {{asmtType}} · {{subjectText}}"
        selector.hasAsmtSubject = true

        # add subjects combination, i.e. Math & ELA
        defaultSubject = "#{this.subjectsData.subject1}_#{this.subjectsData.subject2}"
        defaultSubjectText = "#{this.subjectsData.subject1} & #{this.subjectsData.subject2}"
        selector.defaultSubjectText = defaultSubjectText

        asmts = [{ asmt_subject: defaultSubject, asmt_subject_text: defaultSubjectText }]
        for subject, subject_text of @subjectsData
          asmts.push
            asmt_subject: subject_text
            asmt_subject_text: "#{subject_text} Details"
        selector.asmts = asmts
        selectors.push selector
      selectors


  StudentGrid: StudentGrid
