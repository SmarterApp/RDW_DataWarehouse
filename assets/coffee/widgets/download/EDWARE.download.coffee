define [
  "jquery"
  "bootstrap"
  "mustache"
  "moment"
  "text!CSVOptionsTemplate"
  "text!DownloadMenuTemplate"
  "text!PDFOptionsTemplate"
  "text!SuccessTemplate"
  "text!FailureTemplate"
  "text!NoDataTemplate"
  "edwareConstants"
  "edwareClientStorage"
  "edwarePreferences"
  "edwareExport"
  "edwareDataProxy"
  "edwareUtil"
  "edwareModal"
  "edwareEvents"
], ($, bootstrap, Mustache, moment, CSVOptionsTemplate, DownloadMenuTemplate, PDFOptionsTemplate, SuccessTemplate, FailureTemplate, NoDataTemplate, Constants, edwareClientStorage, edwarePreferences, edwareExport, edwareDataProxy, edwareUtil, edwareModal, edwareEvents) ->

  REQUEST_ENDPOINT = {
    "registrationStatistics": "/services/extract/student_registration_statistics",
    "studentAssessment": "/services/extract",
    "completionStatistics": "/services/extract/student_assessment_completion"
    "rawXML": "/services/extract/raw_data"
    "itemLevel": "/services/extract/assessment_item_level"
  }

  showFailureMessage = (response) ->
    @hide()
    $('#DownloadResponseContainer').html Mustache.to_html FailureTemplate, {
      labels: @config.labels
      options: @config.ExportOptions
    }
    $('#DownloadFailureModal').edwareModal
      keepLastFocus: true

  showSuccessMessage = (response) ->
    @hide()
    download_url = response["download_url"]
    $('#DownloadResponseContainer').html Mustache.to_html SuccessTemplate, {
      labels: @config.labels
      options: @config.ExportOptions
      download_url: download_url
    }
    $('#DownloadSuccessModal').edwareModal
      keepLastFocus: true

  class StateDownloadModal

    constructor: (@container, @config, @reportParamCallback) ->
      @initialize()
      @bindEvents()
      # Bind to Events first, so we get the clicks on default values for free
      @selectDefault()

    initialize: ()->
      output = Mustache.to_html CSVOptionsTemplate, {
        extractType: this.config.extractType
        asmtType: this.config['asmtType']
        subject: this.config['asmtSubject']
        academicYear: this.config['academicYear']
        registrationAcademicYear: this.config['registrationAcademicYear']
        asmtState: this.config['asmtState']
        labels: this.config['labels']
        grade: this.config['grade']
        options: this.config.ExportOptions
      }
      this.container.html output
      this.dropdownMenu = $('ul.dropdown-menu', this.container)
      this.checkboxMenu = $('ul.checkbox-menu', this.container)
      this.submitBtn = $('.edware-btn-primary', this.container)
      this.asmtTypeBox = $('div#asmtType', this.container)
      this.fetchParams =
        completionStatistics: this.getSACParams
        registrationStatistics: this.getSRSParams
        rawXML: this.getAuditXMLItemLevelParams
        itemLevel: this.getAuditXMLItemLevelParams

    bindEvents: ()->
      self = this
      # show or hide componenets on page according export type
      $('.extractType input', @container).click (e) ->
        self.extractType = $(this).attr('value')
        $('#StateDownloadModal .modal-body').removeClass().addClass("#{self.extractType} modal-body")

      # set up academic years
      $('ul.edware-dropdown-menu li', @container).click (e)->
        $this = $(this)
        # hide error message
        $this.closest('.section').removeClass('error')
        display = $this.data('label')
        value = $this.data('value')
        $dropdown = $this.closest('.btn-group')
        $dropdown.find('.dropdown-menu').attr('data-value', value)
        # display selected option
        $dropdown.find('.dropdown-display').html display
        $dropdown.removeClass 'open'
      .keypress (e) ->
        $(this).click() if e.keyCode is 13

      # collapse dropdown menu when focus out
      $('.btn-group', this.container).focuslost ()->
        $(this).removeClass('open')

      this.submitBtn.click ()->
        # get parameters
        params = self.fetchParams[self.extractType].call(self)
        if not params
          self.displayWarningMessage()
          return
        # disable button and all the input checkboxes
        self.disableInput()
        self.sendRequest REQUEST_ENDPOINT[self.extractType], params

    displayWarningMessage: () ->
      $('#grade').closest('div.section').addClass('error')

    getSACParams: () ->
      academicYear = $('#academicYear').data('value')
      return {
        "extractType": "studentAssessmentCompletion"
        "academicYear":  academicYear
      }

    getSRSParams: () ->
      academicYear = $('#registrationAcademicYear').data('value')
      return {
        "extractType": "studentRegistrationStatistics"
        "academicYear":  academicYear
      }

    getAuditXMLItemLevelParams: () ->
      # jQuery.data('attr') function doesn't work for some reason
      grade = String($('#grade').attr('data-value'))
      if not grade
        return false
      academicYear = String($('#academicYear').data('value'))
      asmtSubject = $('input[name="asmtSubject"]:checked').val()
      asmtType = $('input[name="asmtType"]:checked').val()
      return {
        "asmtYear":  academicYear
        "asmtSubject":  asmtSubject
        "asmtType":  asmtType
        "asmtGrade": grade
      }

    getSelectedOptions: ($dropdown)->
      # get selected option text
      checked = []
      $dropdown.find('input:checked').each () ->
        checked.push $(this).data('label')
      optionValue = $dropdown.find('.dropdown-menu').data('value')
      if optionValue
        checked.push optionValue
      checked

    selectDefault: ()->
      # check first option of each dropdown
      $('ul li:nth-child(1) input',this.container).each ()->
        $(this).trigger 'click'

    sendRequest: (url, params)->
      params = $.extend(true, params, this.getParams())

      # Get request time
      currentTime = moment()
      this.requestDate = currentTime.format 'MMM Do'
      this.requestTime = currentTime.format 'h:mma'

      options =
        params: params
        method: 'POST'
        redirectOnError: false

      request = edwareDataProxy.getDatafromSource url, options
      request.done showSuccessMessage.bind(this)
      request.fail showFailureMessage.bind(this)

    hide: () ->
      $('#StateDownloadModal').edwareModal('hide')
      this.submitBtn.removeAttr 'disabled'
      $('input:checkbox', this.container).removeAttr 'disabled'
      $('.btn-extract-academic-year').attr('disabled', false)
      $('button.report_type', self.container).removeAttr 'disabled'

    disableInput: () ->
      this.submitBtn.attr('disabled','disabled')
      $('input:checkbox', this.container).attr('disabled', 'disabled')
      $('.btn-extract-academic-year').attr('disabled', true)
      $('button.report_type', self.container).attr('disabled', 'disabled')

    getParams: ()->
      params = {}
      storageParams = JSON.parse edwareClientStorage.filterStorage.load()
      if storageParams and storageParams['stateCode']
        params['stateCode'] = storageParams['stateCode']

      params

    show: () ->
      $('#StateDownloadModal').edwareModal
        keepLastFocus: true


  class PDFModal

    constructor: (@container, @config) ->
      self = this
      loadingLanguage = edwareDataProxy.getDatafromSource "../data/languages.json"
      loadingLanguage.done (data)->
        languages = for key, value of data.languages
          { key:key, value: value }
        self.initialize languages
        self.bindEvents()
        self.show()

    initialize: (languages) ->
      output = Mustache.to_html PDFOptionsTemplate,
        labels: @config.labels
        languages: languages
        options: @config.ExportOptions
      @container.html output

    bindEvents: () ->
      self = this
      $('#bulkprint').on 'click', ->
        $(this).attr('disabled', 'disabled')
        self.sendPDFRequest()

      # check English by default
      $('input#en').attr('checked', 'checked')

    getParams: () ->
      params = edwarePreferences.getFilters()
      asmt = edwarePreferences.getAsmtPreference()
      # backend expects asmt grades as a list
      grade = params['asmtGrade']
      if grade
        params['asmtGrade'] = [ grade ]
      else
        params['asmtGrade'] = undefined
      params["effectiveDate"] = asmt.effectiveDate
      params["asmtType"] = asmt.asmtType || 'Summative'
      params["asmtYear"] = edwarePreferences.getAsmtYearPreference()

      language = @container.find('input[name="language"]:checked').val()
      # color or grayscale
      mode = @container.find('input[name="color"]:checked').val()
      params["lang"] = language
      params["mode"] = mode
      params

    sendPDFRequest: () ->
      params = @config.getReportParams()
      params = $.extend(@getParams(), params)
      request = edwareDataProxy.sendBulkPDFRequest params
      request.done showSuccessMessage.bind(this)
      request.fail showFailureMessage.bind(this)

    show: () ->
      $('#PDFModal').edwareModal
        keepLastFocus: true

    hide: () ->
      $('#bulkprint').removeAttr('disabled')
      $('#PDFModal').edwareModal('hide')

  class DownloadMenu

    constructor: (@container, @config, @contextSecurity) ->
      @reportType = @config.reportType
      this.initialize(@container)
      this.bindEvents()

    disableInvisibleButtons: () ->
      $('input[type="radio"]:not(:visible)', @container).attr('disabled', 'disabled')

    initialize: (@container) ->
      # Based on the report type, explicitly set the description for enabled and no permission
      if @reportType
        this.config.ExportOptions.export_download_raw_view.desc.enabled = this.config.ExportOptions.export_download_raw_view.desc.enabled[@reportType]
        this.config.ExportOptions.export_download_raw_view.desc.no_permission = this.config.ExportOptions.export_download_raw_view.desc.no_permission[@reportType]
      output = Mustache.to_html DownloadMenuTemplate, {
        reportType: @reportType
        labels: this.config['labels']
        options: this.config.ExportOptions
      }
      $(@container).html output
      this.eventHandler =
        file: this.downloadAsFile
        stateExtract: this.sendStateExtract
        extract: this.sendExtractRequest
        pdf: this.printPDF

    show: () ->
      $('#DownloadMenuModal').edwareModal()

    hide: () ->
      $('#exportButton').removeAttr('disabled')
      $('#DownloadMenuModal').edwareModal('hide')

    bindEvents: () ->
      self = this
      # bind export event
      $('.btn-primary', '#DownloadMenuModal').click ->
        # disable button to avoid user click twice
        $('#exportButton').attr('disabled', 'disabled')
        # get selected option
        option = $(self.container).find('input[type="radio"]:checked').val()
        self.eventHandler[option].call(self)
      $('#DownloadMenuModal').on 'shown', ->
        self.disableInvisibleButtons()

    downloadAsFile: () ->
      # download 508-compliant file
      $('#gridTable').edwareExport @config.reportName, @config.labels
      @hide()

    getParams: ()->
      # extract both Math and ELA summative results
      params = {}
      params['asmtSubject'] = Constants.SUBJECTS
      params['asmtType'] = ['SUMMATIVE']
      asmtYear = edwarePreferences.getAsmtYearPreference()
      params["asmtYear"] =[asmtYear.toString()]
      params['extractType'] = ['studentAssessment']

      storageParams = JSON.parse edwareClientStorage.filterStorage.load()
      if storageParams and storageParams['stateCode']
        params['stateCode'] = [storageParams['stateCode']]

      if storageParams and storageParams['districtGuid']
        params['districtGuid'] = [storageParams['districtGuid']]

      params

    sendAsyncExtractRequest: () ->
      # extract Math and ELA summative assessment data
      params = $.extend(true, {'async': 'true'}, this.getParams())
      # Get request time
      currentTime = moment()
      this.requestDate = currentTime.format 'MMM Do'
      this.requestTime = currentTime.format 'h:mma'

      options =
        params: params
        method: 'POST'
        redirectOnError: false

      request = edwareDataProxy.getDatafromSource REQUEST_ENDPOINT["studentAssessment"], options
      request.done showSuccessMessage.bind(this)
      request.fail showFailureMessage.bind(this)

    sendExtractRequest: () ->
      # perform asynchronous extract on state and distrct level
      if @reportType is Constants.REPORT_TYPE.STATE or @reportType is Constants.REPORT_TYPE.DISTRICT
        this.sendAsyncExtractRequest()
      else
        # perform synchronous extract on school and grade level
        this.sendSyncExtractRequest()
        this.hide()

    sendSyncExtractRequest: () ->
      values = JSON.parse edwareClientStorage.filterStorage.load()
      # Get asmtType from session storage
      asmtType = edwarePreferences.getAsmtPreference().asmtType || Constants.ASMT_TYPE.SUMMATIVE
      # Get filters
      params = edwarePreferences.getFilters()
      # Get sticky compared rows if any
      params = $.extend(@config.getReportParams(), params)
      params['stateCode'] = values['stateCode']
      params['districtGuid'] = values['districtGuid']
      params['schoolGuid'] = values['schoolGuid']
      params['asmtGrade'] = values['asmtGrade'] if values['asmtGrade']
      params['asmtType'] = asmtType.toUpperCase()
      params['asmtSubject'] = edwarePreferences.getSubjectPreference()
      params['asmtYear'] = edwarePreferences.getAsmtYearPreference()
      url = window.location.protocol + "//" + window.location.host + "/services/extract?sync=true&" + $.param(params, true)
      window.location = url

    sendStateExtract: () ->
      @hide()
      CSVOptions = @config.CSVOptions
      CSVOptions.labels = @config.labels
      CSVOptions.ExportOptions = @config.ExportOptions
      reportType = @config.reportType
      reportParamsCallback = @config.getReportParams
      self = this
      # construct CSVDownload modal
      loadingData = fetchData @config.param
      loadingData.done (data)->
        # merge academic years to JSON config
        years = edwareUtil.getAcademicYears data.asmt_period_year
        studentRegYears = edwareUtil.getAcademicYears data.studentRegAcademicYear
        CSVOptions.academicYear.options = years if years
        CSVOptions.registrationAcademicYear.options = studentRegYears if studentRegYears
        # display file download options
        CSVDownload = new StateDownloadModal $('.CSVDownloadContainer'), CSVOptions, reportParamsCallback
        self.contextSecurity?.apply()
        CSVDownload.show()

    printPDF: () ->
      @hide()
      hasData = $('#gridTable').text() isnt ''
      if not hasData
        # display warning message and stop
        @displayWarningMessage()
      else
        @PDFOptionsModal ?= new PDFModal $('.PrintContainer'), @config
        @PDFOptionsModal.show()

    displayWarningMessage: () ->
      output = Mustache.to_html NoDataTemplate,
        labels: @config.labels
        options: @config.ExportOptions
      $('#DownloadResponseContainer').html output
      $('#DownloadFailureModal').edwareModal
        keepLastFocus: true

    fetchData = (params)->
      options =
        method: "POST"
        params: params
        redirectOnError: false
      edwareDataProxy.getDatafromSource "/data/academic_year", options

  create = (container, reportType, config, reportParamCallback)->
    new StateDownloadModal $(container), reportType, config, reportParamCallback

  StateDownloadModal: StateDownloadModal
  DownloadMenu: DownloadMenu
  create: create
