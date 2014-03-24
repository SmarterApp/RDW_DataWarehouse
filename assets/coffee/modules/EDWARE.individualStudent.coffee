#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareConfidenceLevelBar"
  "text!templates/individualStudent_report/individual_student_template.html"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareHeader"
  "edwarePreferences"
  "edwareConstants"
  "edwareReportInfoBar"
  "edwareReportActionBar"
], ($, bootstrap, Mustache, edwareDataProxy, edwareConfidenceLevelBar, indivStudentReportTemplate, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences, Constants, edwareReportInfoBar, edwareReportActionBar) ->

  class DataProcessor

    constructor: (@data, @configData, @isGrayscale) ->

    process: () ->
      @processData()
      @processAccommodations()
      @data

    processAccommodations: () ->
      for asmtType, assessments  of @data.items
        for asmt in assessments
          sections = @buildAccommodations asmt.accommodations
          if sections.length > 0
            asmt.accommodations = {"sections": sections}
          else
            # do not display accommodation at all if none is available
            asmt.accommodations = undefined

    buildAccommodations: (accommodations) ->
      # mapping accommodation code and column name to meaningful description text
      for code, columns of accommodations
        section = {}
        description = @configData.accommodationMapping[code]
        continue if not description
        section["description"] = description
        accommodation = for column in columns
          @configData.accommodationColumns[column]
        section["accommodation"] = accommodation.sort()
        section

    processData: () ->
      # TODO: below code should be made prettier someday
      for asmtType, assessments  of @data.items
        for assessment, idx in assessments
          for cut_point_interval, i in assessment.cut_point_intervals
            if @isGrayscale
              assessment.cut_point_intervals[i] = $.extend(cut_point_interval, @configData.grayColors[i])
            else if not cut_point_interval.bg_color
              # if cut points don't have background colors, then it will use default background colors
              assessment.cut_point_intervals[i] = $.extend(cut_point_interval, @configData.colors[i])

          # Generate unique id for each assessment section. This is important to generate confidence level bar for each assessment
          # ex. assessmentSection0, assessmentSection1
          assessment.count = idx

          # set role-based content
          assessment.content = @configData.content

          # Select cutpoint color and background color properties for the overall score info section
          performance_level = assessment.cut_point_intervals[assessment.asmt_perf_lvl-1]

          # Apply text color and background color for overall score summary info section
          assessment.score_color = performance_level.bg_color
          assessment.score_text_color = performance_level.text_color
          assessment.score_bg_color = performance_level.bg_color
          assessment.score_name = performance_level.name

          # set level-based overall ald content
          overallALD = Mustache.render(this.configData.overall_ald[assessment.asmt_subject], assessment)
          overallALD = edwareUtil.truncateContent(overallALD, edwareUtil.getConstants("overall_ald"))
          assessment.overall_ald = overallALD

          # set psychometric_implications content
          psychometricContent = Mustache.render(this.configData.psychometric_implications[asmtType][assessment.asmt_subject], assessment)

          # if the content is more than character limits then truncate the string and add ellipsis (...)
          psychometricContent = edwareUtil.truncateContent(psychometricContent, edwareUtil.getConstants("psychometric_characterLimits"))
          assessment.psychometric_implications = psychometricContent

          # set policy content
          grade = @configData.policy_content[assessment.grade]
          if grade
            if assessment.grade is "11"
              assessment.policy_content = grade[assessment.asmt_subject]
            else if assessment.grade is "8"
              assessment.policy_content = grade[assessment.asmt_subject][assessment.asmt_perf_lvl]

          for claim in assessment.claims
            claim.subject = assessment.asmt_subject.toUpperCase()
            claim.desc = @configData.claims[assessment.asmt_subject]["description"][claim.indexer]
            # length info is used for bootstrap to determine how many columns for a claim
            claim.length = 12 / assessment.claims.length

  class EdwareISR

    constructor: () ->
      self = this
      loading = edwareDataProxy.getDataForReport Constants.REPORT_JSON_NAME.ISR
      loading.done (configData) ->
        self.configData = configData
        self.initialize()
        self.loadPrintMedia()
        self.fetchData()

    loadPage: (template) ->
      data = JSON.parse(Mustache.render(JSON.stringify(template), @configData))
      @data = new DataProcessor(data, @configData, @isGrayscale).process()
      @data.labels = @configData.labels
      @grade = @data.context.items[4]
      @subjectsData = @data.subjects
      @render()
      @createBreadcrumb()
      @renderReportInfo()
      @renderReportActionBar()
      #Grayscale logo for print version
      if @isGrayscale
        $(".printHeader .logo img").attr("src", "../images/smarter_printlogo_gray.png")

    initialize: () ->
      @params = edwareUtil.getUrlParams()
      @isPdf = @params['pdf']
      @isGrayscale = @params['grayscale']
      @reportInfo = @configData.reportInfo
      @legendInfo = @configData.legendInfo

    getAsmtGuid: () ->
      if not @isPdf
        asmt = edwarePreferences.getAsmtPreference()
        asmt?.asmtGuid

    getCurrentAsmtType: () ->
      if @isPdf
        currentAsmtType = @params['asmtType']
      else
        asmt = edwarePreferences.getAsmtPreference()
        currentAsmtType = asmt?.asmtType
      currentAsmtType || Constants.ASMT_TYPE.SUMMATIVE

    fetchData: () ->
      # Get individual student report data from the server
      self = this
      ISR_REPORT_SERVICE = "/data/individual_student_report"
      loadingData = edwareDataProxy.getDatafromSource ISR_REPORT_SERVICE,
        method: "POST"
        params: @params
      loadingData.done (data) ->
        self.loadPage data

    loadPrintMedia: () ->
      # Show grayscale
      edwareUtil.showGrayScale() if @isGrayscale
      # Load css for pdf generation
      edwareUtil.showPdfCSS() if @isPdf


    createBreadcrumb: () ->
      displayHome = edwareUtil.getDisplayBreadcrumbsHome this.data.user_info
      $('#breadcrumb').breadcrumbs(this.data.context, @configData.breadcrumb, displayHome)

    renderReportInfo: () ->
      edwareReportInfoBar.create '#infoBar',
        reportTitle: $('#individualStudentContent h2.title').text()
        reportName: Constants.REPORT_NAME.ISR
        reportInfoText: @configData.reportInfo
        labels: @labels
        CSVOptions: @configData.CSVOptions
        # subjects on ISR
        subjects: @data.current

    renderReportActionBar: () ->
      currentAsmtType = @getCurrentAsmtType()
      @configData.subject = @createSampleInterval this.data.items[currentAsmtType][0], this.legendInfo.sample_intervals
      @configData.reportName = Constants.REPORT_NAME.ISR
      @configData.asmtTypes = @getAsmtTypes()
      self = this
      @actionBar ?= edwareReportActionBar.create '#actionBar', @configData, () ->
        self.render()
        self.renderReportInfo()

    render: () ->
      asmtType = @getCurrentAsmtType()
      this.data.current = this.data.items[asmtType]
      # use mustache template to display the json data
      output = Mustache.to_html indivStudentReportTemplate, @data
      $("#individualStudentContent").html output

      @updateClaimsHeight()

      # Generate Confidence Level bar for each assessment
      i = 0
      for item, i in @data.items[asmtType]
        barContainer = "#assessmentSection" + i + " .confidenceLevel"
        edwareConfidenceLevelBar.create item, 640, barContainer

        # Set the layout for practical implications and policy content section on print version
        printAssessmentInfoContentLength = 0
        printAssessmentOtherInfo = "#assessmentSection" + i + " li.inline"
        printAssessmentOtherInfoLength = $(printAssessmentOtherInfo).length

        $(printAssessmentOtherInfo).each (index) ->
          printAssessmentInfoContentLength = printAssessmentInfoContentLength + $(this).html().length

        charLimits = 702
        if printAssessmentOtherInfoLength < 2 or printAssessmentInfoContentLength > charLimits
          $(printAssessmentOtherInfo).removeClass "inline"

        if printAssessmentInfoContentLength > charLimits
          assessmentInfo = "#assessmentSection" + i + " .assessmentOtherInfo"
          $(assessmentInfo + " h1").css("display", "block")
          $(".assessmentOtherInfoHeader").addClass("show").css("page-break-before", "always")
          $(assessmentInfo + " li:first-child").addClass("bottomLine")

        i++

      # Show tooltip for claims on mouseover
      $(".arrowBox").popover
        html: true
        container: "#content"
        trigger: "hover"
        placement: (tip, element) ->
          edwareUtil.popupPlacement(element, 400, 276)
        title: ->
          e = $(this)
          e.parent().parent().find(".header").find("h4").html()
        template: '<div class="popover claimsPopover"><div class="arrow"></div><div class="popover-inner large"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
        content: ->
          e = $(this)
          e.find(".claims_tooltip").html() # template location: templates/individualStudent_report/claimsInfo.html

      this.isrHeader = edwareHeader.create(this.data, this.configData) unless this.isrHeader

    updateClaimsHeight: ()->
      ### Update height of all claim box to match the highest one. ###
      for idx, subject of @subjectsData
        do (subject) ->
          descriptions = $(".claims.#{subject.toUpperCase()} .description")
          heights = for desc in descriptions
            $(desc).height()
          highest = Math.max.apply(Math, heights)
          descriptions.height highest

    createSampleInterval : (subject, sample_interval) ->
      # merge sample and subject information
      # the return value will be used to generate legend html page
      subject = $.extend(true, {}, subject, sample_interval)

    getAsmtTypes: () ->
      asmtTypes = []
      for idx, asmt of @data.asmt_administration
        asmt.asmt_type = Constants.ASMT_TYPE[asmt.asmt_type]
        asmt.asmt_subject = @subjectsData[asmt.asmt_subject]
        asmt.display = "{{effectiveDateText}} · {{asmtGrade}} · {{asmtType}}"
        asmt.effective_date = asmt.effective_date
        asmt.asmt_grade = "Grade #{asmt.asmt_grade}"
        asmt.hasAsmtSubject = false
        asmtTypes.push asmt
      asmtTypes


  EdwareISR: EdwareISR
