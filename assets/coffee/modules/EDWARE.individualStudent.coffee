#global define
define [
  "jquery"
  "bootstrap"
  "mustache"
  "edware"
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
  "edwarePopover"
], ($, bootstrap, Mustache, edware, edwareDataProxy, edwareConfidenceLevelBar, isrTemplate, isrInterimBlocksTemplate, edwareBreadcrumbs, edwareUtil, edwareHeader, edwarePreferences, Constants, edwareReportInfoBar, edwareReportActionBar, edwarePopover) ->

  DataFactory = ->

  DataFactory::createDataProcessor = (data, configData, isGrayscale, isBlock) ->
    @dataClass = if isBlock then InterimBlocksDataProcessor else DataProcessor
    new @dataClass data, configData, isGrayscale

  class DataProcessor
    # This is the Data Processor for Summative and Interim Comprehensive
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

    updatePolicyContent: (asmtGrade, subject) ->
      grade = @configData.policy_content[asmtGrade]
      if grade
        if asmtGrade is "11"
          policy_content = grade[subject]
          if @data.metadata?.branding?.higherEdLink
            branding_url = @data.metadata.branding.higherEdLink
            new_link = "<a href='#{branding_url}'>#{branding_url}</a>"
            policy_content = policy_content.replace(@configData.higherEdLinkDefault, new_link)
          @data.printAdditionalInfo ?= {}
          @data.printAdditionalInfo.policy_content ?= policy_content
          policy_content

    updatePsychometricImplications: (asmtType, subject) ->
      @data.printAdditionalInfo ?= {}
      content = this.configData.psychometric_implications[asmtType][subject]
      @data.printAdditionalInfo.psychometric_implications ?= content
      content
    
    processData: () ->
      # TODO: below code should be made prettier someday
      for assessment, idx in @data.all_results
        for cut_point_interval, i in assessment.cut_point_intervals
          # To show the levels as level 1,2,3,4 on pdf
          assessment.cut_point_intervals[i].name = @configData.labels.asmt.perf_lvl_name[i+1]
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
        assessment.score_name = @configData.labels.asmt.perf_lvl_name[assessment.asmt_perf_lvl]

        asmtType = assessment.asmt_type
        if (typeof asmtType is 'string') and (asmtType.toUpperCase() in [Constants.ASMT_TYPE['INTERIM COMPREHENSIVE'].toUpperCase(), Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS'].toUpperCase()])
            assessment.hasInterim = true
        else
            assessment.hasInterim = false
        assessment.invalid = assessment.administration_condition == "IN"
        assessment.standardized = if assessment.administration_condition == "SD" \
            or (assessment.hasInterim and assessment.administration_condition == "") \
            then true else false
        

        # set level-based overall ald content
        overallALD = Mustache.render(this.configData.overall_ald[assessment.asmt_subject][this.configData.overall_ald_grade_buckets[assessment.asmt_grade]][assessment.asmt_perf_lvl], assessment)
        overallALD = edwareUtil.truncateContent(overallALD, edwareUtil.getConstants("overall_ald"))
        assessment.overall_ald = overallALD

        # update assessment_period to be in 'year-year' format instead of 'period year' format
        asmt_year = assessment.asmt_period_year
        assessment.asmt_period = "#{asmt_year-1} - #{asmt_year}"

        # set psychometric_implications content
        psychometricContent = @updatePsychometricImplications assessment.asmt_type, assessment.asmt_subject
        # if the content is more than character limits then truncate the string and add ellipsis (...)
        psychometricContent = edwareUtil.truncateContent(psychometricContent, edwareUtil.getConstants("psychometric_characterLimits"))
        assessment.psychometric_implications = psychometricContent

        # set policy content
        assessment.policy_content = @updatePolicyContent assessment.grade, assessment.asmt_subject

        for claim in assessment.claims
          claim.subject = assessment.asmt_subject.toUpperCase()
          claim.desc = @configData.claims[assessment.asmt_subject]["description"][claim.indexer]
          # length info is used for bootstrap to determine how many columns for a claim
          claim.length = 12 / assessment.claims.length
          claim.name = @configData.labels.asmt[claim.name]
          claim.perf_lvl_name = @configData.labels.asmt[claim.perf_lvl_name]

        key = assessment.date_taken + assessment.asmt_type
        @data['views'] ?= {}
        @data['views'][key] ?= []
        @data['views'][key].push assessment if @data['views'][key].length < 2
        # Important:  This is a workaround for bulk pdf generation
        if assessment.asmt_type is 'Summative'
          default_key = assessment.asmt_period_year + 'Summative'
          @data['views'][default_key] ?= []
          @data['views'][default_key].push assessment if @data['views'][default_key].length < 2


  class InterimBlocksDataProcessor extends DataProcessor
    # This is the Data Processor for Interim Assessment Blocks
    process: () ->
      # Ordering of interim assessment blocks
      @interimAsmtBlocksOrdering = {}
      for k, v of @data.subjects
        @interimAsmtBlocksOrdering[v] = @configData.interimAssessmentBlocksOrdering[k]
      @processData()
      @data

    splitByPerfBlockByName: (asmtSubject, data) ->
      dataByName = {}
      for grade, gradeData of data
        dataByName[grade] ?= {}
        for block in gradeData
          name = block['name']
          dataByName[grade][name]?= {}
          # Get the order in which this block is suppose to be displayed in
          order = @interimAsmtBlocksOrdering[asmtSubject][grade]?.indexOf(block["name"]) || 0 # We don't know about this grade, use 0
          dataByName[grade][name]['displayOrder'] = if order is -1 then @interimAsmtBlocksOrdering[asmtSubject][grade].length else order
          # If a most recent value is not present, set it to the current block
          if not dataByName[grade][name]['mostRecent']
            dataByName[grade][name]['mostRecent'] = block
          else
            placeholder = {'placeholder': true}
            dataByName[grade][name]['previous'] ?= [placeholder, placeholder, placeholder]
            dataByName[grade][name]['previousCounter'] ?= 0
            prevCounter = dataByName[grade][name]['previousCounter']
            if prevCounter < 3
              dataByName[grade][name]['previous'][prevCounter] = block
              dataByName[grade][name]['previousCounter'] +=1
            else
              dataByName[grade][name]['hasOlder'] = true
              dataByName[grade][name]['older'] ?= []
              dataByName[grade][name]['older'].push block

      # Group them back to a list and sort them
      returnData = {}
      for grade, gradeData of dataByName
        returnData[grade] = []
        for k, v of gradeData
          returnData[grade].push(v)
        returnData[grade].sort (x, y) ->
          return -1 if x.displayOrder < y.displayOrder
          return 1 if x.displayOrder > y.displayOrder
          0
        data[grade] = {"blocks": returnData[grade]}

    processData: () ->
      @data['views'] ?= {}
      asmt_year = @data.all_results.asmt_period_year
      # We want to traverse by subject order
      for subjectAlias in Object.keys(@data.subjects).sort()
        subjectName = @data.subjects[subjectAlias]
        subjectData = {}
        dataByGrade = {}
        grades = []
        subjectData['asmt_subject'] = subjectName
        subjectData['asmt_type'] = @data.all_results.asmt_type
        subjectData['asmt_subject_text'] = Constants.SUBJECT_TEXT[subjectName]
        subjectData['asmt_period'] = @data.all_results['asmt_period_year'] - 1 + " - " + @data.all_results['asmt_period_year']
        # Separate all the interim blocks by asmt_grades
        for assessment in @data.all_results[subjectAlias]
          asmt_grade = assessment['grade']
          dataByGrade[asmt_grade] ?= []
          grades.push(asmt_grade) if grades.indexOf(asmt_grade) < 0
          block_info = {'grade': @configData.labels.grade + " " + asmt_grade,
          'date_taken': edwareUtil.formatDate(assessment['date_taken']),
          'name': assessment['claims'][0]['name'],
          'desc': assessment['claims'][0]['perf_lvl_name'],
          'level': assessment['claims'][0]['perf_lvl']}
          dataByGrade[asmt_grade].push(block_info)
        @splitByPerfBlockByName(subjectName, dataByGrade)
        subjectData['grades'] = []
        for grade in grades.sort().reverse()
          subjectData['grades'].push dataByGrade[grade]
          @updatePolicyContent grade, subjectName
        # Keeps track of the views available according to subject.  Used to toggle between subjects in action bar
        subjectData.has_data = true if subjectData.grades.length > 0
        @updatePsychometricImplications subjectData['asmt_type'], subjectName
        @data['views'][asmt_year + @data.all_results.asmt_type]?= []
        @data['views'][asmt_year + @data.all_results.asmt_type].push subjectData


  class EdwareISR

    constructor: () ->
      self = this
      loading = edwareDataProxy.getDataForReport Constants.REPORT_JSON_NAME.ISR
      loading.done (configData) ->
        self.configData = configData
        self.initialize()
        self.loadPrintMedia()
        self.fetchData()

    loadDisclaimer: () ->
      if @isPdf
        asmtType = if @params['asmtType'] then @params['asmtType'].toUpperCase() else edwarePreferences.getAsmtType()
      #Display only for 2 asmt types
      if (typeof asmtType is 'string') and (asmtType.toUpperCase() in [Constants.ASMT_TYPE['INTERIM COMPREHENSIVE'].toUpperCase(), Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS'].toUpperCase()])
        this.configData.interimDisclaimer

    loadPage: (template) ->
      data = JSON.parse(Mustache.render(JSON.stringify(template), @configData))
      @dataFactory ?= new DataFactory()
      @data = @dataFactory.createDataProcessor(data, @configData, @isGrayscale, @isBlock).process()
      @data.labels = @configData.labels
      @data.interimDisclaimer = @loadDisclaimer()
      @grade = @data.context.items[4]
      @academicYears = data.asmt_period_year
      @subjectsData = @data.subjects
      @reloadReport()
      @createBreadcrumb(@data.labels)
      @renderReportInfo()
      @renderReportActionBar()
      # We have to call updateView on first load since action bar hasn't been created yet
      @updateView()

    initialize: () ->
      @tries = 0
      @prepareParams()
      edwarePreferences.saveStateCode @params['stateCode']
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
      # TODO: Check if there is a more elegant way for iab
      subjects = if not @isBlock then @data.current else {}
      edwareReportInfoBar.create '#infoBar',
        reportTitle: $('#individualStudentContent h2').first().text()
        reportName: Constants.REPORT_NAME.ISR
        reportInfoText: @configData.reportInfo
        breadcrumb: @data.context
        labels: @labels
        CSVOptions: @configData.CSVOptions
        metadata: @data.metadata
        # subjects on ISR
        subjects: subjects, false, null

    onAsmtTypeSelected: (asmt) ->
      # save assessment type
      edwarePreferences.saveAsmtForISR(asmt)
      this.prepareParams()
      @reloadReport()

    renderReportActionBar: () ->
      @configData.subject = @createSampleInterval @data.current?[0], this.legendInfo.sample_intervals
      @configData.reportName = Constants.REPORT_NAME.ISR
      self = this
      @configData.asmtTypes =
        options: self.data.asmt_administration
        callback: self.onAsmtTypeSelected.bind self
      @configData.switchView = (asmtView)->
        self.updateView(asmtView)
      @actionBar ?= edwareReportActionBar.create '#actionBar', @configData, @params.asmtType
      # viewName
      @getAsmtViewSelection()

    getCacheKey: ()->
      # For summative and interim comp, it's always dateTaken + asmtType
      # For iab, it's always the asmtYear + asmtType
      if @isPdf
        asmtType = @params['asmtType'].toUpperCase() if @params['asmtType']
        asmtType = Constants.ASMT_TYPE[asmtType] || Constants.ASMT_TYPE.SUMMATIVE
        if asmtType isnt Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS']
          # Important:  This is a workaround for bulk pdf generation
          key = if @params['dateTaken'] then @params['dateTaken'] else @params['asmtYear']
        else
          key = @params['asmtYear']
        return key + asmtType
      else
        asmt = edwarePreferences.getAsmtForISR()
        if asmt and asmt['asmt_type']
          key = if asmt['asmt_type'] isnt Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS'] then @params['dateTaken'] else + asmt['asmt_period_year']
          return key + asmt['asmt_type']
        else
          asmt = @data.asmt_administration[0]
          asmtType = Constants.ASMT_TYPE[asmt['asmt_type']]
          return asmt['date_taken'] + asmtType

    prepareParams: () ->
      params = edwareUtil.getUrlParams()
      @isPdf = params['pdf']
      if not @isPdf
        isrAsmt = edwarePreferences.getAsmtForISR()
        # Read from storage (dropdown change, page reload, ISR isnt reset from student list)
        if isrAsmt and Object.keys(isrAsmt).length isnt 0
          asmtType = isrAsmt['asmt_type']
          asmtYear = isrAsmt['asmt_period_year']
          dateTaken = isrAsmt['date_taken']
          params['asmtType'] = asmtType.toUpperCase() if asmtType
          params['dateTaken'] = dateTaken if dateTaken
          params['asmtYear'] = asmtYear if asmtYear
        else
          # Save ISRasmt to storage
          edwarePreferences.saveAsmtForISR
            asmt_type: Constants.ASMT_TYPE[params['asmtType']]
            date_taken: params['dateTaken']
            asmt_period_year: params['asmtYear']
      @isBlock = if params['asmtType'] is 'INTERIM ASSESSMENT BLOCKS' then true else false
      @params = params

    updateView: () ->
      if not @isPdf
        viewName = @getAsmtViewSelection()
        $("#subjectSelection#{viewName}").addClass('selected')
        $("#individualStudentContent").removeClass("Math").removeClass("ELA").addClass(viewName)

    reloadReport: () ->
      # Decide if we have the data or needs to retrieve from backend
      # It is possible to enter an infinite loop if the cacheKey has a mismatch
      cacheKey = @getCacheKey()
      if not @data['views']?[cacheKey]
        this.prepareParams()
        this.fetchData()
        @tries += 1
        # This is a safety measure incase we have mismatch with the cachekey to prevent infinite loop
        if @tries > 2
          location.href = edwareUtil.getErrorPage()
      else
        @data.current = @data['views'][cacheKey]
        @tries = 0
        @render()
        @updateView()

    render: () ->
      # Get tenant level branding
      @data.branding = edwareUtil.getTenantBrandingDataForPrint @data.metadata, @isGrayscale
      if @isBlock
        @renderInterimBlockView()
      else
        # use mustache template to display the json data
        output = Mustache.to_html isrTemplate, @data
        $("#individualStudentContent").html output

        @updateClaimsHeight()

        # Generate Confidence Level bar for each assessment
        for item, i in @data.current
          # For toggling between subjects
          noResultsMessage = '<div class="no_data screenContent"><p>' + this.data.labels.no_results + '</p></div>'
          subjectMath = $("#individualStudentContent > .Math").attr('class')
          subjectEla = $("#individualStudentContent > .ELA").attr('class')
          $("#individualStudentContent").append(noResultsMessage) and $('.no_data').addClass("Math") if subjectMath is undefined
          $("#individualStudentContent").append(noResultsMessage) and $('.no_data').addClass("ELA") if subjectEla is undefined
          
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
      # fix ELA claim height 0 bug fix
      ela_display = $('#individualStudentContent.Math .ELA')
      math_display = $('#individualStudentContent.ELA .Math')
      ela_display.css('display', 'block')
      math_display.css('display', 'block')
      for idx, subject of @subjectsData
        do (subject) ->
          descriptions = $(".claims.#{subject.toUpperCase()} .description")
          heights = for desc in descriptions
            $(desc).height()
          highest = Math.max.apply(Math, heights)
          descriptions.height highest
      ela_display.css('display','')
      math_display.css('display','')

    createSampleInterval : (subject, sample_interval) ->
      # merge sample and subject information
      # the return value will be used to generate legend html page
      subject = $.extend(true, {}, subject, sample_interval)

    getAsmtViewSelection: () ->
      viewName = edwarePreferences.getAsmtView()
      viewName = @subjectsData['subject1'] if viewName not in Constants.SUBJECTS  # In ISR, we only have two views
      viewName

    renderInterimBlockView: () ->
      @data.labels.older_display_text = if @isPdf then @data.labels.more_dates_online else @data.labels.older
      output = Mustache.to_html isrInterimBlocksTemplate, @data
      isrContent = $("#individualStudentContent")
      isrContent.html output
      if not @isPdf
        @createPopovers()
      else
        # For PDFs we need to hide sections when we have no data
        subjectsWithData = []
        for subjectData in @data.current
          if subjectData.has_data
            subjectsWithData.push subjectData.asmt_subject
        if subjectsWithData.length isnt Object.keys(@data.subjects).length
          isrContent.addClass(subjectName) for subjectName in subjectsWithData

    createPopovers: () ->
      # Creates popovers for interim assessment blocks
      edwarePopover.createPopover
        source: ".olderResults"
        target: "iabPopoverContent"
        contentContainer: ".oldResultsContent"

  EdwareISR: EdwareISR
