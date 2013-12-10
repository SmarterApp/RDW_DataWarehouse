define [
  "jquery"
  "mustache"
  "text!PrintTemplate"
  "edwarePreferences"
], ($, Mustache, PrintTemplate, edwarePreferences) ->

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
      asmtType = $('#selectedAsmtType').text()
      url = document.URL.replace("indivStudentReport","print")
      url = url.replace("#","")
      url += '&pdf=true'
      url += "&grayscale=true" if option is "grayscale"
      url += "&asmtType=" + encodeURI(asmtType) if asmtType
      url += "&lang=" + edwarePreferences.getSelectedLanguage()
      window.open(url, "_blank",'toolbar=0,location=0,menubar=0,status=0,resizable=yes')

    show: () ->
      $('#PrintModal').modal('show')

    hide: () ->
      $('#PrintModal').modal('hide')
    
  create = (container) ->
    new PrintModal(container)
  
  create: create
  PrintModal: PrintModal
