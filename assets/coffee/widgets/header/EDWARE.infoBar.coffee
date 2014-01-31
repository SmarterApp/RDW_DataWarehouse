define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
  "edwarePopover"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload, edwarePopover) ->

  class ReportInfoBar

    constructor: (@container, @config) ->
      #TODO how to specify what information expected?
      this.initialize()
      this.bindEvents()

    initialize: () ->
      $(this.container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
      this.createDownloadMenu() if not this.edwareDownloadMenu

    bindEvents: () ->
      self = this
      # show download menu
      $('.downloadIcon').click ->
        self.edwareDownloadMenu.show()

      # bind report info popover
      $('.reportInfoIcon').edwarePopover
        class: 'reportInfoPopover'
        content: @config.reportInfoText
      # set report info text
      $('.reportInfoWrapper').append @config.reportInfoText

    createDownloadMenu: () ->
      this.edwareDownloadMenu = new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config)

  create = (container, config) ->
    new ReportInfoBar(container, config)

  ReportInfoBar: ReportInfoBar
  create: create
