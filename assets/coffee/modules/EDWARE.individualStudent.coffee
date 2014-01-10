#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareConfidenceLevelBar"
  "edwareClaimsBar"
  "text!templates/individualStudent_report/individual_student_template.html"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareHeader"
  "edwarePreferences"
  "edwareConstants"
  "edwareReportInfoBar"
  "edwareReportActionBar"
], ($, bootstrap, Mustache, edwareDataProxy, edwareConfidenceLevelBar, edwareClaimsBar, indivStudentReportTemplate, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences, Constants, edwareReportInfoBar, edwareReportActionBar) ->

  # claim score weight in percentage
  claimScoreWeightArray = {
    "MATH": ["40", "40", "20", "10"],
    "ELA": ["40", "30", "20", "10"]
  }

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
      @data = JSON.parse(Mustache.render(JSON.stringify(template), @configData))
      @data.labels = @configData.labels
      @grade = @data.context.items[3]
      @subjectsData = @data.subjects
      @processData()
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

    processData: () ->
      for asmtType, assessments  of @data.items
        for assessment, idx in assessments
          for cut_point_interval, i in assessment.cut_point_intervals
            if @isGrayscale
              assessment.cut_point_intervals[i] = $.extend(cut_point_interval, @configData.grayColors[i])
            else if not cut_point_interval
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
          # TODO check grade 11, 8 policy content length, should show up to 256 characters
          grade = @configData.policy_content[assessment.grade]
          if grade
            if assessment.grade is "11"
              assessment.policy_content = grade[assessment.asmt_subject]
            else if assessment.grade is "8"
              assessment.policy_content = grade[assessment.asmt_subject][assessment.asmt_perf_lvl]

          # Add claim score weight
          for claim, j in assessment.claims
            claim.assessmentUC = assessment.asmt_subject.toUpperCase()
            claim.claim_score_weight = claimScoreWeightArray[claim.assessmentUC][j]
            claim.desc = @configData.claims[assessment.asmt_subject]["description"][claim.indexer]
            claim.score_desc = @configData.claims[assessment.asmt_subject]["scoreTooltip"][claim.indexer]


    createBreadcrumb: () ->
      $('#breadcrumb').breadcrumbs(this.data.context, @configData.breadcrumb)

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

      this.renderClaimScoreRelativeDifference asmtType

      # Generate Confidence Level bar for each assessment
      i = 0
      while i < this.data.items[asmtType].length
        item = this.data.items[asmtType][i]
        barContainer = "#assessmentSection" + i + " .confidenceLevel"
        edwareConfidenceLevelBar.create item, 640, barContainer

        j = 0
        while j < item.claims.length
          claim = item.claims[j]
          barContainer = "#assessmentSection" + i + " #claim" + [claim.indexer] + " .claimsBar"
          edwareClaimsBar.create claim, 300, barContainer
          j++


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

      this.isrHeader = edwareHeader.create(this.data, this.configData, "individual_student_report") unless this.isrHeader

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

    #
    # render Claim Score Relative Difference (arrows)
    #
    renderClaimScoreRelativeDifference : (asmtType) ->
      i = 0
      while i < this.data.items[asmtType].length
        items = this.data.items[asmtType][i]
        # find grand parent element ID
        assessmentSectionId = '#assessmentSection' + i
        claims = items.claims
        j = 0
        while j < claims.length
          claim = claims[j]
          # if relative difference is 0, draw diamond on the dashed line, positive, then render uppder div
          if claim.claim_score_relative_difference == 0
            this.drawUpArrow(assessmentSectionId, claim.indexer, 0)
            this.drawDownArrow(assessmentSectionId, claim.indexer, 0)
          else if claim.claim_score_relative_difference > 0
            this.drawUpArrow(assessmentSectionId, claim.indexer, claim.claim_score_relative_difference)
          else
            this.drawDownArrow(assessmentSectionId, claim.indexer, claim.claim_score_relative_difference)
          j++
        i++

    # draw down triangle and arrow on target <div/>
    #
    drawUpArrow : (assessmentSectionId, indexer, claim_score_relative_difference) ->
      # find arraw drawing box ID
      claimArrowBox = assessmentSectionId + ' #claim' + indexer + ' #content' + indexer + '_upper'
      # style for vertical bar
      bar_height = claim_score_relative_difference
      image_y_position = 100 - claim_score_relative_difference

      img = 'Claim_arrowhead_up'
      # style for vertical bar
      arrow_bar_class = "claim_score_arrow_bar claim_score_up_arrow_bar"
      this.drawArrow(claimArrowBox, img, image_y_position, arrow_bar_class, bar_height)

    #
    # draw down triangle and arrow on target <div/>
    #
    drawDownArrow : (assessmentSectionId, indexer, claim_score_relative_difference) ->
      # find arraw drawing box ID
      claimArrowBox = assessmentSectionId + ' #claim' + indexer + ' #content' + indexer + '_lower'
      img = 'Claim_arrowhead_down'
      bar_height = Math.abs(claim_score_relative_difference)
      image_y_position = Math.abs(claim_score_relative_difference)
      # style for vertical bar
      arrow_bar_class = "claim_score_arrow_bar claim_score_down_arrow_bar"
      this.drawArrow(claimArrowBox, img, image_y_position, arrow_bar_class, bar_height)

    # draw triangle and arrow on target <div/>
    #
    drawArrow : (claimArrowBox, triangle_img, triangle_y_position, arrow_bar_class, bar_height) ->
      claimArrowBox_width = $(claimArrowBox).width()
      claimArrowBox_height = $(claimArrowBox).height()
      image_height = 5
      arrow_bar_width = 12
      arrow_bar = $('<div/>')
      arrow_bar.addClass arrow_bar_class
      arrow_bar_center = (claimArrowBox_width/2-arrow_bar_width/2)/claimArrowBox_width*100
      arrow_bar.css("left", arrow_bar_center + "%")
      #"-2" to adjust height of bar perfectly.
      adjusted_bar_height = (bar_height*(claimArrowBox_height-image_height*2-2)/100)/(claimArrowBox_height-image_height*2)*100
      arrow_bar.css("height", adjusted_bar_height + "%")
      # set Triangle image in target div
      $(claimArrowBox).addClass(triangle_img)
      $(claimArrowBox).attr("style", "background-position: 50% " + triangle_y_position + "% !important")
      $(claimArrowBox).append arrow_bar

    getAsmtTypes: () ->
      asmtTypes = []
      for idx, asmt of @data.asmt_administration
        asmt.asmt_type = Constants.ASMT_TYPE[asmt.asmt_type]
        asmt.asmt_subject = @subjectsData[asmt.asmt_subject]
        asmt.display = "#{asmt.asmt_year} · #{@grade.name} · #{asmt.asmt_type}"
        asmt.hasAsmtSubject = false
        asmtTypes.push asmt
      asmtTypes


  EdwareISR: EdwareISR
