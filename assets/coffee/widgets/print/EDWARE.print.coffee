define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!PrintTemplate"
  "edwarePreferences"
  "edwareUtil"
], ($, bootstrap, Mustache, PrintTemplate, edwarePreferences, edwareUtil) ->

  class PrintModal

    constructor: (@container) ->
      @initialize()
      @bindEvents()

    initialize: () ->
      output = Mustache.to_html PrintTemplate, {}
      $(@container).html output

    bindEvents: () ->
      self = this
      # print button click event
      $('.btn-primary', @container).click ->
        self.print()

    print: () ->
      @hide()
      option = $('input[name=print]:checked', @container).val()
      asmtType = edwarePreferences.getAsmtType()
      params = edwareUtil.getUrlParams()
      url = edwareUtil.getBaseURL() + "/assets/html/print.html?"
      url += 'studentGuid=' + params['studentGuid']
      url += '&stateCode=' + params['stateCode']
      url += '&pdf=true'
      url += "&grayscale=true" if option is "grayscale"
      url += "&asmtType=" + encodeURI(asmtType) if asmtType
      url += "&lang=" + edwarePreferences.getSelectedLanguage()
      url += "&effectiveDate=" + edwarePreferences.getEffectiveDate()
      window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')

    show: () ->
      $('#PrintModal').modal('show')

    hide: () ->
      $('#PrintModal').modal('hide')

  create = (container) ->
    new PrintModal(container)

  create: create
  PrintModal: PrintModal
