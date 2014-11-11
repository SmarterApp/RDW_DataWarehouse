define [
  "jquery"
  "bootstrap"
  "mustache"
  "edware"
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
  "edwarePopover"
], ($, bootstrap, Mustache, edware, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences,  Constants, edwareStickyCompare, edwareReportInfoBar, edwareReportActionBar, contextSecurity, edwareSearch, edwareFilter, edwarePopover) ->

  LOS_HEADER_BAR_TEMPLATE  = $('#edwareLOSHeaderConfidenceLevelBarTemplate').html()

  EdwareGridStickyCompare = edwareStickyCompare.EdwareGridStickyCompare

  class StudentModel

    constructor: (@asmtType, @effectiveDate, @dataSet) ->

    init: (row) ->
      @appendColors row
      row = @appendExtraInfo row
      row

    appendColors: (assessment) ->
      # display asssessment type in the tooltip title
      for key, value of @dataSet.subjectsData
        value = assessment[key]
        continue if not value
        # display asssessment type in the tooltip title
        subjectType = @dataSet.subjectsData[key]
        value.asmt_type = subjectType
        # do not continue to process if cut point data is unavailable
        continue if not @dataSet.cutPointsData
        cutpoint = @dataSet.cutPointsData[key]
        $.extend value, cutpoint
        # set default colors for out of range asmt_perf_lvl
        if value.asmt_perf_lvl > value.cut_point_intervals.length
          value.score_bg_color = "#D0D0D0"
          value.score_text_color = "#000000"
        else
          value.score_bg_color = value.cut_point_intervals[value.asmt_perf_lvl - 1]?.bg_color
          value.score_text_color = value.cut_point_intervals[value.asmt_perf_lvl - 1]?.text_color

    appendExtraInfo: (row) ->
      # Format student name
      row['student_full_name'] = edwareUtil.format_full_name_reverse row['student_first_name'], row['student_middle_name'], row['student_last_name']
      # This is for links in drill down
      row['params'] = {
        "studentId": row['student_id'],
        "stateCode": row['state_code'],
        "asmtYear": edwarePreferences.getAsmtYearPreference(),
        'asmtType': encodeURI(@asmtType.toUpperCase()),
      }
      row['params']['effectiveDate'] ?= @effectiveDate if @effectiveDate
      row

  class StudentDataSet

    constructor: (@config) ->
      @asmtTypes = config.students.customViews.asmtTypes

    build: (@data, @cutPointsData, @labels) ->
      @cache = {}
      @allSubjects = "#{data.subjects.subject1}_#{data.subjects.subject2}"
      @assessmentsData  = data.assessments
      @subjectsData = data.subjects

      asmtType = edwarePreferences.getAsmtType()
      if asmtType is Constants.ASMT_TYPE.IAB
        @formatIABData()
      else
        @formatAssessmentsData()

    getColumnData: (viewName) ->
      asmtType = edwarePreferences.getAsmtType() || Constants.ASMT_TYPE.SUMMATIVE
      if asmtType is Constants.ASMT_TYPE.IAB and viewName is @allSubjects
        viewName = 'Math'  #TODO:
      return @columnData[asmtType][viewName][0]["items"][0]["field"]

    getColumns: (viewName) ->
      asmt = edwarePreferences.getAsmtPreference()
      asmtType = asmt.asmt_type || Constants.ASMT_TYPE.SUMMATIVE
      @createColumns(asmtType, viewName)

    createColumns: (asmtType, viewName) ->
      if asmtType is Constants.ASMT_TYPE.IAB
        @createColumnsIAB()[viewName]
      else
        @createColumnsSummativeInterim()[viewName]

    createColumnsIAB: () ->
      currentGrade = @config.grade.id
      columnData = JSON.parse(Mustache.render(JSON.stringify(@config.students_iab)))
      for subject, columns of @data.interim_assessment_blocks
        subjectName = @data.subjects[subject]
        for claim in @config.interimAssessmentBlocksOrdering[subject][currentGrade]
          effective_dates = columns[claim]
          if not effective_dates
            continue
          isExpanded = edwarePreferences.isExpandedColumn(claim)
          for effective_date, i in effective_dates
            titleText = if isExpanded then edwareUtil.formatDate(effective_date) else claim
            if titleText.length > 27
              titleText = titleText[..27] + "..."
            iab_column_details = {
              titleText: titleText
              subject: subject
              claim: claim
              expanded: isExpanded
              numberOfColumns: Object.keys(effective_dates).length
              effectiveDate: effective_date
              i: i
              width: if isExpanded then 98 else 140
            }
            column = JSON.parse(Mustache.render(JSON.stringify(@config.column_for_iab), iab_column_details))
            columnData[subjectName][0].items.push column
            # only show latest effective date if not expanded
            if not isExpanded
              break
      columnData

    createColumnsSummativeInterim: () ->
      if not @data.metadata
        return
      claimsData = JSON.parse(Mustache.render(JSON.stringify(@data.metadata.claims), @data))
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
            row = new StudentModel(asmtType, effectiveDate, this).init assessment
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

    formatIABData: () ->
      @cache[Constants.ASMT_TYPE.IAB] ?= {}
      for asmtType, studentList of @assessmentsData
        for studentId, assessment of studentList
          continue if assessment.hide
          row = new StudentModel(Constants.ASMT_TYPE.IAB, null, this).init assessment
          # push to each subject view
          for subjectName, subjectType of @subjectsData
            continue if not row[subjectName] or row[subjectName].hide
            @cache[Constants.ASMT_TYPE.IAB][subjectType] ?= []
            @cache[Constants.ASMT_TYPE.IAB][subjectType].push row

    getAsmtData: (viewName, params)->
      asmt = edwarePreferences.getAsmtPreference()
      asmtType = asmt.asmt_type
      if asmtType is Constants.ASMT_TYPE.IAB
        return @getIAB(params, viewName)
      else
        return @getSummativeAndInterim(asmt, viewName)

    getIAB: (params, viewName) ->
      viewName = viewName || Constants.ASMT_VIEW.MATH
      data = @cache[Constants.ASMT_TYPE.IAB][viewName]
      data

    getSummativeAndInterim: (asmt, viewName) ->
      viewName = viewName || Constants.ASMT_VIEW.OVERVIEW
      effectiveDate = asmt.effective_date
      asmtType = asmt.asmt_type
      data = @cache[effectiveDate]?[asmtType]?[viewName]
      if data
        for item in data
          item.assessments = item[asmtType]
      data


  class StudentGrid

    constructor: (@config) ->
      @isLoaded = true
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
      total_groups = @data.groups
      if total_groups.length > 0
        group_filter = configs.group_template
        for group in total_groups
          group_filter.options.push group
        configs.filters.push group_filter
      return configs

    loadPage: (@data) ->
      @cutPointsData = @createCutPoints()
      @contextData = data.context
      @subjectsData = data.subjects
      @userData = data.user_info
      @academicYears = data.asmt_period_year
      @config.grade = @contextData['items'][4]
      @renderBreadcrumbs(@labels)
      @renderReportInfo()
      @renderReportActionBar()
      @renderFilter()
      @createHeaderAndFooter()

      @bindEvents()
      @applyContextSecurity()

    applyContextSecurity: ()->
      # init context security
      contextSecurity.init @data.context.permissions, @config, Constants.REPORT_TYPE.GRADE
      contextSecurity.apply()

    createCutPoints: () ->
      cutPointsData = @data.metadata?.cutpoints
      cutPointsData = JSON.parse(Mustache.render(JSON.stringify(cutPointsData),@data)) if cutPointsData
      #if cut points don't have background colors, then it will use default background colors
      for key, items of cutPointsData
        for interval, i in items.cut_point_intervals
          if not interval.bg_color
            $.extend(interval, @config.colors[i])
      cutPointsData

    bindEvents: ()->
      $document = $(document)
      # Show tooltip for overall score on mouseover
      $document.on
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

      # expandable icons
      self = this
      $document.off Constants.EVENTS.EXPAND_COLUMN
      $document.on Constants.EVENTS.EXPAND_COLUMN, (e, source)->
        e.stopPropagation()
        $this = $(source)
        columnName = $this.parent().attr('title') || $this.siblings('a').attr('title')
        if $this.hasClass("edware-icon-collapse-expand-plus")
          $this.removeClass("edware-icon-collapse-expand-plus").addClass("edware-icon-collapse-expand-minus")
          edwarePreferences.saveExpandedColumns(columnName)
        else
          $this.removeClass("edware-icon-collapse-expand-minus").addClass("edware-icon-collapse-expand-plus")
          edwarePreferences.removeExpandedColumns(columnName)
        offset = $('.ui-jqgrid-bdiv').scrollLeft()
        self.updateView(offset)

    createHeaderAndFooter: () ->
      self = this
      this.header = edwareHeader.create(this.data, this.config) unless this.header

    fetchExportData: () ->
      this.assessmentsData

    renderBreadcrumbs: (labels) ->
      displayHome = edwareUtil.getDisplayBreadcrumbsHome this.data.user_info
      $('#breadcrumb').breadcrumbs(@contextData, @config.breadcrumb, displayHome, labels)

    renderReportInfo: () ->
      # placeholder text for search box
      @config.labels.searchPlaceholder = @config.searchPlaceholder
      @config.labels.SearchResultText = @config.SearchResultText
      @infoBar ?= edwareReportInfoBar.create '#infoBar',
        breadcrumb: @contextData
        reportTitle: "Students in #{@contextData.items[4].name}"
        reportType: Constants.REPORT_TYPE.GRADE
        reportName: Constants.REPORT_NAME.LOS
        reportInfoText: @config.reportInfo
        labels: @labels
        CSVOptions: @config.CSVOptions
        ExportOptions: @config.ExportOptions
        metadata: @data.metadata
        param: @params
        academicYears:
          options: @academicYears
          callback: @onAcademicYearSelected.bind(this)
        getReportParams: @getReportParams.bind(this), true, contextSecurity

    getReportParams: () ->
      params = {}
      studentIDs = @stickyCompare.getRows()
      params["studentId"] = studentIDs if studentIDs.length isnt 0
      params

    onAcademicYearSelected: (year) ->
      edwarePreferences.clearAsmtPreference()
      @params['asmtYear'] = year
      @params['asmtType'] = Constants.ASMT_TYPE.SUMMATIVE.toUpperCase()
      @reload @params

    onAsmtTypeSelected: (asmt) ->
      edwarePreferences.saveAsmtForISR(asmt)
      edwarePreferences.saveAsmtPreference asmt
      @params['asmtType'] = asmt.asmt_type.toUpperCase()
      @reload @params

    renderReportActionBar: () ->
      self = this
      @config.colorsData = @cutPointsData
      @config.reportName = Constants.REPORT_NAME.LOS
      @config.academicYears =
        options: @academicYears
        callback: @onAcademicYearSelected.bind(this)
      @config.asmtTypes =
        options: @data.asmt_administration
        callback: @onAsmtTypeSelected.bind(this)
      @config.switchView = @updateView.bind(this)
      @actionBar = edwareReportActionBar.create '#actionBar', @config

    createGrid: (filters) ->
      asmtType = edwarePreferences.getAsmtType()
      filterFunc = edwareFilter.createFilter(filters)(asmtType)
      data = filterFunc(@data)
      @studentsDataSet.build data, @cutPointsData, @labels
      @updateView()
      #TODO: Set asmt Subject
      subjects = []
      for key, value of @data.subjects
        subjects.push value
      edwarePreferences.saveSubjectPreference subjects

    updateView: (offset) ->
      viewName = edwarePreferences.getAsmtView()
      viewName = viewName || Constants.ASMT_VIEW.OVERVIEW
      asmtType = edwarePreferences.getAsmtType()
      $('#gridWrapper').removeClass().addClass("#{viewName} #{Constants.ASMT_TYPE[asmtType]}")
      $("#subjectSelection#{viewName}").addClass('selected')
      @renderGrid viewName
      @renderReportInfo().updateAsmtTypeView()
      @createPrintMedia()
      $('.ui-jqgrid-bdiv').scrollLeft(offset) if offset

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
      this.infoBar.update()
      @createPopovers()

    renderGrid: (viewName) ->
      $('#gridTable').jqGrid('GridUnload')
      asmtData = @studentsDataSet.getAsmtData(viewName, @params)
      columns = @studentsDataSet.getColumns(viewName)
      fieldName = Constants.INDEX_COLUMN.LOS
      filteredInfo = @stickyCompare.getFilteredInfo(asmtData, fieldName)
      
      self = this
      edwareGrid.create {
        data: filteredInfo.data
        columns: columns
        options:
          labels: self.labels
          scroll: false
          frozenColumns: true
          expandableColumns: true
          stickyCompareEnabled: filteredInfo.enabled
          gridComplete: () ->
            self.afterGridLoadComplete()
      }
      @updateTotalNumber(filteredInfo.data?.length)
      @renderHeaderPerfBar()
      $(document).trigger Constants.EVENTS.SORT_COLUMNS

    updateTotalNumber: (total) ->
      reportType = Constants.REPORT_TYPE.GRADE
      display = "#{total} #{@labels.next_level[reportType]},"
      $('#total_number').text display

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

    createPopovers: () ->
      # Creates popovers for interim assessment blocks
      edwarePopover.createPopover
        source: ".hasOlderResults"
        target: "iabPopoverContent"
        contentContainer: ".oldResultsContent"
        container: "#content"

    createPrintMedia: () ->
      $('#gview_gridTable_print_media').remove()
      gview_gridTable_h = $($('#gview_gridTable .ui-jqgrid-hdiv table').get(0))
      gview_gridTable_b = $($('#gview_gridTable .ui-jqgrid-bdiv table').get(0))
      table_width = gview_gridTable_h.outerWidth()
      page_width =  $('body').width()
      pageCount = Math.ceil(table_width / page_width)
      $('#gridWrapper').append('<div id="gview_gridTable_print_media" class="printContent ui-jqgrid ui-widget ui-widget-content ui-corner-all"></div>')
      printWrap = $('#gview_gridTable_print_media')
      i = 0
      while i < pageCount
        $('<div>&nbsp;</div>').appendTo(printWrap) if i isnt 0
        $('<div class="pageBreak">').appendTo(printWrap) if i isnt 0
        printPage = $('<div class="ui-jqgrid-hbox"></div>').css(overflow: "hidden", width: page_width, "page-break-before": (if i is 0 then "auto" else "always")).appendTo(printWrap)
        if i+1 is pageCount
          printPage.css('margin-bottom', '40px')
        gview_gridTable_h.clone().appendTo(printPage).css({"position": "relative", "left": -i * page_width})
        gview_gridTable_b.clone().appendTo(printPage).css({"position": "relative", "left": -i * page_width})
        i++

  StudentGrid: StudentGrid
  
