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

    constructor: (@data, @configData, @isGrayscale, @isBlock) ->

    process: () ->
      if not @isBlock
        @processData()
        @processAccommodations()
      else
        # Ordering of interim assessment blocks
        @interimAsmtBlocksOrdering = {}
        for k, v of @data.subjects
            @interimAsmtBlocksOrdering[v] = @configData.interimAssessmentBlocksOrdering[k]
        @processInterimBlocksData()
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

    divideInterimBlocksData: (data) ->
      # Divide into blocks of 3s for display purposes
      value = {"row": []}
      blocks = []
      for i in data
        blocks.push i
      size = data.length / 3
      dividedBlocks = []
      for j in [0..size-1]
        b = blocks.slice(3 * j, 3 * (j+1))
        dividedBlocks.push({"blocks": b})
      value["row"] = dividedBlocks
      value

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
        # After Sorting, divide it for display purposes
        data[grade] = @divideInterimBlocksData returnData[grade]
    
    formatDate: (date) ->
      date.substring(0, 4) + "." + date.substring(4, 6) + "." + date.substring(6)
       
    processInterimBlocksData: () ->
      @data['views'] ?= {}
      for subjectAlias, subjectName of @data.subjects
        subjectData = {}
        dataByGrade = {}
        grades = []
        # Separate all the interim blocks by asmt_grades
        for assessment in @data.all_results[subjectAlias]
          asmt_grade = assessment['grade']
          dataByGrade[asmt_grade] ?= [] 
          grades.push(asmt_grade) if grades.indexOf(asmt_grade) < 0
          block_info = {'grade': @configData.labels.grade + " " + asmt_grade, 
          'effective_date': @formatDate(assessment['effective_date']), 
          'name': assessment['claims'][0]['name'], 
          'desc': assessment['claims'][0]['perf_lvl_name'], 
          'level': assessment['claims'][0]['perf_lvl']}
          dataByGrade[asmt_grade].push(block_info)
        @splitByPerfBlockByName(subjectName, dataByGrade)
        subjectData['grades'] = []
        for grade in grades.sort().reverse()
          subjectData['grades'].push dataByGrade[grade]
        # Keeps track of the views available according to subject.  Used to toggle between subjects in action bar
        @data['views'][subjectName] = subjectData
  
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
      @isBlock = if @params['asmtType'] is 'INTERIM ASSESSMENT BLOCKS' then true else false
      @data = new DataProcessor(data, @configData, @isGrayscale, @isBlock).process()
      @data.labels = @configData.labels
      @grade = @data.context.items[4]
      @academicYears = data.asmt_period_year
      @subjectsData = @data.subjects
      @render()
      @createBreadcrumb(@data.labels)
      @renderReportInfo()
      @renderReportActionBar()
      @bindEvents()

    initialize: () ->
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

    bindEvents: () ->
      $(document).on
        'mouseenter focus': ->
          elem = $(this)
          elem.popover
            html: true
            trigger: "manual"
            container: '#iabPopoverContent'
            placement: (tip, element) ->
              edwareUtil.popupPlacement(element, 400, 200)
            template: '<div class="popover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"></div></div></div>'
            content: ->
              elem.parent().find(".oldResultsContent").html()
          .popover("show")
        click: (e) ->
          e.preventDefault()
        'mouseleave focusout': ->
          elem = $(this)
          elem.popover("hide")
      , ".olderResults"
   
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
      # TODO:  Currently, the data format is different for interim blocks which the following check, ideally, we should unify it
      sample = @data.current?[0] || {}
      @configData.subject = @createSampleInterval sample, this.legendInfo.sample_intervals
      @configData.reportName = Constants.REPORT_NAME.ISR
      @configData.asmtTypes = @data.asmt_administration

      self = this
      @actionBar ?= edwareReportActionBar.create '#actionBar', @configData, (asmt) ->
        # save assessment type
        edwarePreferences.saveAsmtForISR(asmt)
        self.updateView()
        self.renderReportInfo()
      @getAsmtViewSelection()
    
    getCacheKey: ()->
      if @isPdf
        asmtType = @params['asmtType'].toUpperCase() if @params['asmtType']
        asmtType = Constants.ASMT_TYPE[asmtType] || Constants.ASMT_TYPE.SUMMATIVE
        if @params['effectiveDate']
          return @params['effectiveDate'] + asmtType
        else
          return @params['asmtYear'] + asmtType
      else
        asmt = edwarePreferences.getAsmtForISR()
        if asmt
          if asmt['asmt_type'] isnt Constants.ASMT_TYPE['INTERIM ASSESSMENT BLOCKS'] 
            return asmt['effective_date'] + asmt['asmt_type']
          else
            # TODO: read it from somewhere else
            return edwarePreferences.getAsmtView()
        else
          asmt = @data.asmt_administration[0]
          asmtType = Constants.ASMT_TYPE[asmt['asmt_type']]
          return asmt['effective_date'] + asmtType

    prepareParams: () ->
      params = edwareUtil.getUrlParams()
      @isPdf = params['pdf']
      if not @isPdf
        isrAsmt = edwarePreferences.getAsmtForISR()
        if isrAsmt
          asmtType = isrAsmt['asmt_type']
          effectiveDate = isrAsmt['effective_date']
        params['asmtType'] = asmtType.toUpperCase() if asmtType
        params['effectiveDate'] = effectiveDate if effectiveDate
      else
        params['asmtType'] = params['asmtType'].toUpperCase() if params['asmtType']
      @params = params
    
    updateView: () ->
      cacheKey = @getCacheKey()
      if not @data['views']?[cacheKey]
        this.prepareParams()
        this.fetchData()
      else
        this.render()
      
    render: () ->
      # Get tenant level branding
      @data.branding = edwareUtil.getTenantBrandingDataForPrint @data.metadata, @isGrayscale

      # The template for Interim Block is different
      if @isBlock
        @renderInterimBlockView()
      else
        cacheKey = @getCacheKey()
        @data.current = @data[cacheKey]

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

    getAsmtViewSelection: () ->
      viewName = edwarePreferences.getAsmtView()
      $("#subjectSelection#{viewName}").addClass('selected')

      # TODO: remove this css change after we fix ISR for summative/interim to have subject buttons
      style = if not @isBlock then 'none' else 'inline-block'
      $('.detailsItem').css('display', style)

      viewName

    renderInterimBlockView: () ->
      viewName = @getAsmtViewSelection()
      @data.current = @data['views'][viewName]
      # Update subject text and asmt period year that is unique according to the view
      @data.all_results.asmt_subject_text = Constants.SUBJECT_TEXT[viewName]
      @data.all_results.asmt_period = @data.all_results['asmt_period_year'] - 1 + " - " + @data.all_results['asmt_period_year']
      output = Mustache.to_html isrInterimBlocksTemplate, @data
      $("#individualStudentContent").html output
        
     
  EdwareISR: EdwareISR
