define [
  "jquery"
  "bootstrap"
  "mustache"
  "moment"
  "text!CSVOptionsTemplate"
  "text!DownloadMenuTemplate"
  "text!PDFOptionsTemplate"
  "text!PDFSuccessTemplate"
  "text!PDFNoDataTemplate"
  "edwareConstants"
  "edwareClientStorage"
  "edwarePreferences"
  "edwareExport"
  "edwareDataProxy"
  "edwareUtil"
  "edwareModal"
  "edwareEvents"
], ($, bootstrap, Mustache, moment, CSVOptionsTemplate, DownloadMenuTemplate, PDFOptionsTemplate, PDFSuccessTemplate, PDFNoDataTemplate, Constants, edwareClientStorage, edwarePreferences, edwareExport, edwareDataProxy, edwareUtil, edwareModal, edwareEvents) ->

  ERROR_TEMPLATE = $(CSVOptionsTemplate).children('#ErrorMessageTemplate').html()

  SUCCESS_TEMPLATE = $(CSVOptionsTemplate).children('#SuccessMessageTemplate').html()

  INDIVIDUAL_VALID_TEMPLATE = $(CSVOptionsTemplate).children('#IndividualValidationTemplate').html()

  COMBINED_VALID_TEMPLATE = $(CSVOptionsTemplate).children('#CombinedValidationTemplate').html()

  TEST_NAME = {"studentRegistrationStatistics": "Student Registration Statistics", "studentAssessment": "Tests Results", "studentRegistrationCompletion": "Student Registration Completion"}

  REQUEST_ENDPOINT = {
    "studentRegistrationStatistics": "/services/extract/student_registration_statistics",
    "studentAssessment": "/services/extract",
    "studentRegistrationCompletion": "/services/extract/student_registration_completion"
  }


  class CSVDownloadModal

    constructor: (@container, @config) ->
      this.initialize()
      this.bindEvents()

    initialize: ()->
      this.container = $(this.container)
      output = Mustache.to_html CSVOptionsTemplate, {
        extractType: this.config['extractType']
        asmtType: this.config['asmtType']
        subject: this.config['asmtSubject']
        asmtYear: this.config['asmtYear']
        academicYear: this.config['academicYear']
        studentRegAcademicYear: this.config['studentRegAcademicYear']
        asmtState: this.config['asmtState']
        labels: this.config['labels']
        options: this.config.ExportOptions
      }
      this.container.html output
      this.message = $('#message', this.container)
      this.dropdownMenu = $('ul.dropdown-menu', this.container)
      this.checkboxMenu = $('ul.checkbox-menu', this.container)
      this.submitBtn = $('.edware-btn-primary', this.container)
      this.asmtTypeBox = $('div#asmtType', this.container)
      this.selectDefault()
      this.reportTypes = for option in @config.extractType.options
        option.value
      this.setMainPulldownLabel(@reportTypes[0])

    bindEvents: ()->
      self = this
      # prevent dropdown menu from disappearing
      $('ul.dropdown-menu.report_type li', @container).click (e) ->
        $('div.error', self.messages).remove()
        reportType = $(this).data('value')
        self.setMainPulldownLabel(reportType)

      # set up academic years
      $('ul.edware-dropdown-menu li', @container).click (e)->
        $this = $(this)
        display = $this.data('label')
        value = $this.data('value')
        $dropdown = $this.closest('.btn-group')
        $dropdown.find('.dropdown-menu').attr('data-value', value)
        # display selected option
        $dropdown.find('.dropdown-display').html display
        $dropdown.removeClass 'open'
      .keypress (e) ->
        $(this).click() if e.keyCode is 13


      $('input:checkbox', this.container).click (e)->
        $this = $(this)
        $dropdown = $this.closest('.btn-group')
        # remove earlier error messages
        $('div.error', self.messages).remove()
        if not self.validate($dropdown)
          $dropdown.addClass('invalid')
          self.showNoneEmptyMessage $dropdown.data('option-name')
        else
          $dropdown.removeClass('invalid')

      # collapse dropdown menu when focus out
      $('.btn-group', this.container).focuslost ()->
        $(this).removeClass('open')

      this.submitBtn.click ()->
        # remove earlier error messages
        $('div.error', self.messages).remove()
        # validate each selection group
        invalidFields = []
        # check if button is 'Close' or 'Request'
        if $(this).data('dismiss') != 'modal'
          $('tr:visible div.btn-group', self.container).each ()->
            $dropdown = $(this)
            if not self.validate($dropdown)
              $dropdown.addClass('invalid')
              invalidFields.push $dropdown.data('option-name')
          if invalidFields.length isnt 0
            self.showCombinedErrorMessage invalidFields
          else
            # disable button and all the input checkboxes
            self.disableInput()
            self.sendRequest REQUEST_ENDPOINT[self.reportType]

    setMainPulldownLabel: (reportType)->
      @reportType = reportType
      $('#CSVModal').removeClass(@reportTypes.join(" ")).addClass(reportType)

    validate: ($dropdown) ->
      isValid  = false
      if this.reportType is 'studentRegistrationStatistics'
        isValid = this.validate_sr_options $dropdown
      else
        isValid = this.validate_input_options $dropdown
      isValid

    validate_input_options: ($dropdown) ->
      checked = this.getSelectedOptions $dropdown
      checked.length isnt 0

    validate_sr_options: ($dropdown) ->
      checked = []
      if $('#studentRegAcademicYear .dropdown-display').text() != ""
        checked.push $('#studentRegAcademicYear .dropdown-display').text()
      allChecked = checked.concat this.getSelectedOptions $dropdown
      allChecked.length isnt 0

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

    sendRequest: (url)->
      params = $.extend(true, {'async': 'true'}, this.getParams())
      # Get request time
      currentTime = moment()
      this.requestDate = currentTime.format 'MMM Do'
      this.requestTime = currentTime.format 'h:mma'

      options =
        params: params
        method: 'POST'
        redirectOnError: false

      request = edwareDataProxy.getDatafromSource url, options
      request.done this.showSuccessMessage.bind(this)
      request.fail this.showFailureMessage.bind(this)

    toDisplay: (item)->
      # convert server response to display text
      # create key and display text mapping
      configMap = {}
      for key, value of this.config
        if key isnt 'labels' and key isnt 'ExportOptions'
          for option in value.options
            configMap[option.value] = option.display
      for key, value of item
        item[key] = configMap[value] if configMap[value]
      item

    showCloseButton: () ->
      this.submitBtn.text 'Close'
      this.submitBtn.removeAttr 'disabled'
      this.submitBtn.attr 'data-dismiss', 'modal'

    enableInput: () ->
      this.submitBtn.removeAttr 'disabled'
      $('input:checkbox', this.container).removeAttr 'disabled'
      $('.btn-extract-academic-year').attr('disabled', false)
      $('button.report_type', self.container).removeAttr 'disabled'

    disableInput: () ->
      this.submitBtn.attr('disabled','disabled')
      $('input:checkbox', this.container).attr('disabled', 'disabled')
      $('.btn-extract-academic-year').attr('disabled', true)
      $('button.report_type', self.container).attr('disabled', 'disabled')

    showSuccessMessage: (response)->
      taskResponse = response['tasks'].map this.toDisplay.bind(this)
      fileName = response['fileName']

      downloadUrl = response['download_url']
      success = taskResponse.filter (item)->
        item['status'] is 'ok'
      failure = taskResponse.filter (item)->
        item['status'] is 'fail'
      if success.length > 0
        this.showCloseButton()
      else
        this.enableInput()

      this.message.html Mustache.to_html SUCCESS_TEMPLATE, {
        requestTime: this.requestTime
        requestDate: this.requestDate
        fileName: fileName
        downloadUrl: downloadUrl
        testName: TEST_NAME[this.reportType]
        # success messages
        success: success
        singleSuccess: success.length == 1
        multipleSuccess: success.length > 1
        # failure messages
        failure: failure
        singleFailure: failure.length == 1
        multipleFailure: failure.length > 1
      }

    showFailureMessage: (response)->
      this.enableInput()
      errorMessage = Mustache.to_html ERROR_TEMPLATE, {
        response: response
      }
      this.message.append errorMessage
      this.asmtTypeBox.addClass('invalid')

    showNoneEmptyMessage: (optionName)->
      validationMsg = Mustache.to_html INDIVIDUAL_VALID_TEMPLATE, {
        optionName: optionName.toLowerCase()
      }
      this.message.append validationMsg

    showCombinedErrorMessage: (optionNames)->
      validationMsg = Mustache.to_html COMBINED_VALID_TEMPLATE, {
        optionNames: optionNames
      }
      this.message.append validationMsg

    getParams: ()->
      params = {}
      $('tr:visible ul.checkbox-menu', this.container).each (index, param)->
        $param = $(param)
        key = $param.data('key')
        params[key] = []
        $param.find('input:checked').each ()->
          params[key].push $(this).attr('value')

      $('tr:visible ul.dropdown-menu', this.container).each (index, param)->
        $this = $(this)
        key = $this.data('key')
        value = $this.data('value')
        if key is 'academicYear'
          params[key] = [value]
        else
          params[key] = [value.toString()]

      storageParams = JSON.parse edwareClientStorage.filterStorage.load()
      if storageParams and storageParams['stateCode']
        params['stateCode'] = [storageParams['stateCode']]
      params

    show: () ->
      $('#CSVModal').edwareModal
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
      request.done @showSuccessMessage.bind(this)
      request.fail @showFailureMessage.bind(this)

    showFailureMessage: () ->
      $('#bulkprint').removeAttr('disabled')

    showSuccessMessage: (response) ->
      @hide()
      download_url = response["download_url"]
      $('#PDFSuccessContainer').html Mustache.to_html PDFSuccessTemplate, {
        labels: @config.labels
        options: @config.ExportOptions
        download_url: download_url
      }
      $('#PDFSuccessModal').edwareModal
        keepLastFocus: true

    show: () ->
      $('#PDFModal').edwareModal
        keepLastFocus: true

    hide: () ->
      $('#bulkprint').removeAttr('disabled')
      $('#PDFModal').edwareModal('hide')

  class DownloadMenu

    constructor: (@container, @config) ->
      this.initialize(@container)
      this.bindEvents()

    disableInvisibleButtons: () ->
      $('input[type="radio"]:not(:visible)', @container).attr('disabled', 'disabled')

    initialize: (@container) ->
      output = Mustache.to_html DownloadMenuTemplate, {
        labels: this.config['labels']
        options: this.config.ExportOptions
      }
      $(@container).html output
      this.eventHandler =
        file: this.downloadAsFile
        csv: this.sendCSVRequest
        extract: this.sendExtractRequest
        pdf: this.printPDF

    show: () ->
      $('#DownloadMenuModal').edwareModal()

    hide: () ->
      $('#DownloadMenuModal').edwareModal('hide')

    bindEvents: () ->
      self = this
      # bind export event
      $('.btn-primary', '#DownloadMenuModal').click ->
        # get selected option
        option = $(self.container).find('input[type="radio"]:checked').val()
        self.eventHandler[option].call(self)
        self.hide()
      $('#DownloadMenuModal').on 'shown', ->
        self.disableInvisibleButtons()

    downloadAsFile: () ->
      # download 508-compliant file
      $('#gridTable').edwareExport @config.reportName, @config.labels

    sendExtractRequest: () ->
      values = JSON.parse edwareClientStorage.filterStorage.load()
      # Get asmtType from session storage
      asmtType = edwarePreferences.getAsmtPreference().asmtType || Constants.ASMT_TYPE.SUMMATIVE
      params = {}
      params['stateCode'] = values['stateCode']
      params['districtGuid'] = values['districtGuid']
      params['schoolGuid'] = values['schoolGuid']
      params['asmtGrade'] = values['asmtGrade'] if values['asmtGrade']
      params['asmtType'] = asmtType.toUpperCase()
      params['asmtSubject'] = edwarePreferences.getSubjectPreference()
      params['asmtYear'] = edwarePreferences.getAsmtYearPreference()
      url = window.location.protocol + "//" + window.location.host + "/services/extract?sync=true&" + $.param(params, true)
      window.location = url

    sendCSVRequest: () ->
      CSVOptions = @config.CSVOptions
      CSVOptions.labels = @config.labels
      CSVOptions.ExportOptions = @config.ExportOptions
      # construct CSVDownload modal
      loadingData = fetchData @config.param
      loadingData.done (data)->
        # merge academic years to JSON config
        years = edwareUtil.getAcademicYears data.asmt_period_year
        studentRegYears = edwareUtil.getAcademicYears data.studentRegAcademicYear
        CSVOptions.asmtYear.options = years if years
        CSVOptions.academicYear.options = years if years
        CSVOptions.studentRegAcademicYear.options = studentRegYears if studentRegYears
        # display file download options
        CSVDownload = new CSVDownloadModal $('.CSVDownloadContainer'), CSVOptions
        CSVDownload.show()

    printPDF: () ->
      hasData = $('#gridTable').text() isnt ''
      if not hasData
        # display warning message and stop
        @displayWarningMessage()
      else
        @PDFOptionsModal ?= new PDFModal $('.PrintContainer'), @config
        @PDFOptionsModal.show()

    displayWarningMessage: () ->
      output = Mustache.to_html PDFNoDataTemplate,
        labels: @config.labels
        options: @config.ExportOptions
      $('#PDFFailureContainer').html output
      $('#PDFFailureModal').edwareModal
        keepLastFocus: true


    fetchData = (params)->
      options =
        method: "POST"
        params: params
      edwareDataProxy.getDatafromSource "/data/academic_year", options

  create = (container, config)->
    new CSVDownloadModal $(container), config

  CSVDownloadModal: CSVDownloadModal
  DownloadMenu: DownloadMenu
  create: create
