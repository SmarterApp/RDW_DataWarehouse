define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!PrintTemplate"
  "edwarePreferences"
  "edwareUtil"
  "edwareModal"
], ($, bootstrap, Mustache, PrintTemplate, edwarePreferences, edwareUtil, edwareModal) ->

  class PrintModal

    constructor: (@container, @labels) ->
      @initialize()
      @bindEvents()

    initialize: () ->
      output = Mustache.to_html PrintTemplate, @labels
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
      url += "&mode=color" if option is "color"
      url += "&asmtType=" + encodeURI(asmtType) if asmtType
      url += "&lang=" + edwarePreferences.getSelectedLanguage()
      url += "&effectiveDate=" + edwarePreferences.getEffectiveDate()
      window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')

    show: () ->
      $('#PrintModal').edwareModal()

    hide: () ->
      $('#PrintModal').edwareModal('hide')

  create = (container, labels) ->
    new PrintModal(container, labels)

  create: create
  PrintModal: PrintModal
