define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload) ->

  class ReportInfoBar
  
    constructor: (@container, @config) ->
      #TODO how to specify what information expected?
      this.initialize()
      this.bindEvents()

    initialize: () ->
      $(this.container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
      this.createDownloadMenu() if not this.edwareDownloadMenu
        
    bindEvents: () ->
      self = this
      # show download menu
      $('.downloadIcon').click ->
        self.edwareDownloadMenu.show()
      # back button click event
      $('.backButton').click ->
        history.back()
      # bind report info popover
      $('.reportInfoIcon').popover
        html: true
        placement: 'bottom'
        trigger: 'hover'
        container: '#content'
        content: @config.reportInfoText

    createDownloadMenu: () ->
      this.edwareDownloadMenu = new edwareDownload.DownloadMenu('#downloadMenuPopup', @config)

  create = (container, config) ->
    new ReportInfoBar(container, config)

  ReportInfoBar: ReportInfoBar
  create: create