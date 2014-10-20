#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edwareDataProxy"
  "edwareConfidenceLevelBar"
  "text!templates/individualStudent_report/individual_student_template.html"
  "text!templates/individualStudent_report/individual_student_interim_blocks_template.html"
  "edwareBreadcrumbs"
  "edwareUtil"
  "edwareHeader"
  "edwarePreferences"
  "edwareConstants"
  "edwareReportInfoBar"
  "edwareReportActionBar"
], ($, bootstrap, Mustache, edwareDataProxy, edwareConfidenceLevelBar, isrTemplate, isrInterimBlocksTemplate, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences, Constants, edwareReportInfoBar, edwareReportActionBar) ->

  class DataProcessor

    constructor: (@data, @configData, @isGrayscale) ->

    process: () ->
      @processData()
      @processAccommodations()
      @data

    processAccommodations: () ->
      for asmt in this.data.all_results
        sections = @buildAccommodations asmt.accommodations
        if sections.length > 0
          asmt.accommodations = {"sections": sections}
        else
          # do not display accommodation at all if none is available
          asmt.accommodations = undefined

    buildAccommodations: (accommodations) ->
      # mapping accommodation code and column name to meaningful description text
      accommodations_enhanced = {}
      for code, columns of accommodations
        bucket = @configData.accomodationCodeBuckets[code]
        accommodation_codes = accommodations_enhanced[bucket] || []
        accommodation_codes = accommodation_codes.concat accommodations[code]
        accommodations_enhanced[bucket] = accommodation_codes

      keys = Object.keys(accommodations_enhanced).sort() 
      for code in keys
        columns = accommodations_enhanced[code]
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
      for assessment, idx in @data.all_results
        for cut_point_interval, i in assessment.cut_point_intervals
          if @isGrayscale
            assessment.cut_point_intervals[i] = $.extend(cut_point_interval, @configData.grayColors[i])
          else if not cut_point_interval.bg_color
            # if cut points don't have background colors, then it will use default background colors
            assessment.cut_point_intervals[i] = $.extend(cut_point_interval, @configData.colors[i])

        # Generate unique id for each assessment section. This is important to generate confidence level bar for each assessment
        # ex. assessmentSection0, assessmentSection1
        assessment.count = idx

        # map subject to meaningful text
        assessment.asmt_subject_text = Constants.SUBJECT_TEXT[assessment.asmt_subject]

        # set role-based content
        assessment.content = @configData.content

        # Select cutpoint color and background color properties for the overall score info section
        performance_level = assessment.cut_point_intervals[assessment.asmt_perf_lvl-1]

        # Apply text color and background color for overall score summary info section
        assessment.score_color = performance_level.bg_color
        assessment.score_text_color = performance_level.text_color
        assessment.score_bg_color = performance_level.bg_color
        assessment.score_name = @configData.labels.asmt[performance_level.name]

        # set level-based overall ald content
        overallALD = Mustache.render(this.configData.overall_ald[assessment.asmt_subject], assessment)
        overallALD = edwareUtil.truncateContent(overallALD, edwareUtil.getConstants("overall_ald"))
        assessment.overall_ald = overallALD

        # update assessment_period to be in 'year-year' format instead of 'period year' format
        asmt_year = assessment.asmt_period_year
        assessment.asmt_period = "#{asmt_year-1} - #{asmt_year}"

        # set psychometric_implications content
        psychometricContent = Mustache.render(this.configData.psychometric_implications[assessment.asmt_type][assessment.asmt_subject], assessment)

        # if the content is more than character limits then truncate the string and add ellipsis (...)
        psychometricContent = edwareUtil.truncateContent(psychometricContent, edwareUtil.getConstants("psychometric_characterLimits"))
        assessment.psychometric_implications = psychometricContent

        # set policy content
        grade = @configData.policy_content[assessment.grade]
        if grade
          if assessment.grade is "11"
            policy_content = grade[assessment.asmt_subject]
            if @data.metadata?.branding?.higherEdLink
                branding_url = @data.metadata.branding.higherEdLink
                new_link = "<a href='#{branding_url}'>#{branding_url}</a>"
                policy_content = policy_content.replace(@configData.higherEdLinkDefault, new_link)
            assessment.policy_content = policy_content

        for claim in assessment.claims
          claim.subject = assessment.asmt_subject.toUpperCase()
          claim.desc = @configData.claims[assessment.asmt_subject]["description"][claim.indexer]
          # length info is used for bootstrap to determine how many columns for a claim
          claim.length = 12 / assessment.claims.length
          claim.name = @configData.labels.asmt[claim.name]
          claim.perf_lvl_name = @configData.labels.asmt[claim.perf_lvl_name]

        key = assessment.effective_date + assessment.asmt_type
        @data[key] ?= []
        @data[key].push assessment if @data[key].length < 2
        #TODO: temporary workaround for bulk pdf generation
        if assessment.asmt_type is 'Summative'
          default_key = assessment.asmt_period_year + 'Summative'
          @data[default_key] ?= []
          @data[default_key].push assessment if @data[default_key].length < 2


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
      @academicYears = data.asmt_period_year
      @subjectsData = @data.subjects
      @render()
      @createBreadcrumb(@data.labels)
      @renderReportInfo()
      @renderReportActionBar()

    initialize: () ->
      @params = edwareUtil.getUrlParams()
      edwarePreferences.saveStateCode @params['stateCode']
      @isPdf = @params['pdf']
      @isGrayscale = @params['grayscale']
      @reportInfo = @configData.reportInfo
      @legendInfo = @configData.legendInfo

    getAsmtGuid: () ->
      if not @isPdf
        asmt = edwarePreferences.getAsmtPreference()
        asmt?.asmtGuid

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


    createBreadcrumb: (labels) ->
      displayHome = edwareUtil.getDisplayBreadcrumbsHome this.data.user_info
      $('#breadcrumb').breadcrumbs(this.data.context, @configData.breadcrumb, displayHome, labels)

    renderReportInfo: () ->
      edwareReportInfoBar.create '#infoBar',
        reportTitle: $('#individualStudentContent h2.title').text()
        reportName: Constants.REPORT_NAME.ISR
        reportInfoText: @configData.reportInfo
        breadcrumb: @data.context
        labels: @labels
        CSVOptions: @configData.CSVOptions
        metadata: @data.metadata
        # subjects on ISR
        subjects: @data.current, false, null

    renderReportActionBar: () ->
      @configData.subject = @createSampleInterval this.data.current[0], this.legendInfo.sample_intervals
      @configData.reportName = Constants.REPORT_NAME.ISR
      @configData.asmtTypes = @data.asmt_administration

      self = this
      @actionBar ?= edwareReportActionBar.create '#actionBar', @configData, (asmt) ->
        # save assessment type
        edwarePreferences.saveAsmtForISR(asmt)
        self.render()
        self.renderReportInfo()

    getCacheKey: ()->
      if @isPdf
        asmtType = @params['asmtType'].toUpperCase() if @params['asmtType']
        asmtType = Constants.ASMT_TYPE[asmtType] || Constants.ASMT_TYPE.SUMMATIVE
        if @params['effectiveDate']
          return {"key": @params['effectiveDate'] + asmtType}
        else
          return {"key": @params['asmtYear'] + asmtType}
      else
        asmt = edwarePreferences.getAsmtForISR()
        if asmt
          if asmt['asmt_type'] isnt Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS'] 
            return {"key": asmt['effective_date'] + asmt['asmt_type']} 
          else
            # Special case for Interim blocks as we need to lazy load from server
            return {"isInterimBlock": true, "asmt_period_year": asmt['asmt_period_year'], "asmt_type": asmt['asmt_type']}
        else
          asmt = @data.asmt_administration[0]
          asmtType = Constants.ASMT_TYPE[asmt['asmt_type']]
          return {"key": asmt['effective_date'] + asmtType}

    render: () ->
      cacheKey = @getCacheKey()
      if not cacheKey['isInterimBlock']
        @data.current = @data[cacheKey['key']]
      else
        # For interim blocks, we need to lazy load from BE
        newParams = $.extend(true, {'asmtPeriodYear': cacheKey['asmt_period_year']}, @params)
        # TODO: Fetch data from server
        # TEMP - we need to get the data for legend (action bar)
        @data.current = @data['20160106Interim Comprehensive']
        @sortInterimBlocksData("Math", 3)
        tmpData = {"student_full_name": "Matt Sollars", 
        "asmt_grade": "Grade 5",
        "asmt_subject": "Mathematics", 
        "asmt_subject_text": "Mathematics",
        "asmt_type": "Interim Assessment Blocks",
        "asmt_period": "2014 - 2015", 
        "grade": [ {"blocks": [
          {"block": [{"indexer": "0", "grade": "Grade 7", "name": "Ratio and Proportional Relationships", "level": "1", "desc": "Above Standard", "effective_date": "2014.05.05"}, 
                      {"indexer": "1", "grade": "Grade 7", "name": "Number System", "level": "3","desc": "Above Standard", "effective_date": "2014.05.05"}, 
                      {"indexer": "2", "grade": "Grade 7", "name": "Expressions and Equations", "level": "2","desc": "Above Standard", "effective_date": "2014.05.05"}]},
          {"block": [{"indexer": "3", "grade": "Grade 7", "name": "Statistics and Probability", "level": "1","desc": "Above Standard", "effective_date": "2014.05.05"},
          {"indexer": "4", "grade": "Grade 7", "name": "Mathematics Performance", "level": "1","desc": "Above Standard", "effective_date": "2014.05.05"}]}]},
          {"blocks": [{"block": [{"indexer": "8", "grade": "Grade 6", "name": "Ratio and Proportional Relationships", "level": "1","desc": "Above Standard", "effective_date": "2014.05.05"}]}]}]}
        output = Mustache.to_html isrInterimBlocksTemplate, tmpData
        $("#individualStudentContent").html output
        
      # TEMP ... this needs to be updated
      if not cacheKey['isInterimBlock']
        # Get tenant level branding
        @data.branding = edwareUtil.getTenantBrandingDataForPrint @data.metadata, @isGrayscale
        # use mustache template to display the json data
        output = Mustache.to_html isrTemplate, @data
        $("#individualStudentContent").html output
  
        @updateClaimsHeight()
  
        # Generate Confidence Level bar for each assessment
        i = 0
        for item, i in @data.current
          barContainer = "#assessmentSection" + item.count + " .confidenceLevel"
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

    sortInterimBlocksData : (asmtSubject, asmtGrade)->
      # Given a particular grade's blocks, sort it
      
      # Save this per report
      ordering = {}
      for k, v of @subjectsData
        if asmtSubject is v
          ordering[v] = @configData.interimAssessmentBlocksOrdering[k]
      
      data = [{"name": "Doris"}, {"name": "Fractions"}, {"name": "Functions"}, {"name": "Operations and Algebraic Thinking"}, {"name": "Probability"}]
      for i in data
        order = ordering[asmtSubject][asmtGrade].indexOf(i["name"])
        i['order'] = if order is -1 then ordering[asmtSubject][asmtGrade].length else order
      data.sort (x, y) ->
        return -1 if x.order < y.order
        return 1 if x.order > y.order
        0
      data
     
     
  EdwareISR: EdwareISR
