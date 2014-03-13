define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
  "edwarePopover"
  "edwareYearDropdown"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload, edwarePopover, edwareYearDropdown) ->

  class ReportInfoBar

    constructor: (@container, @config) ->
      #TODO how to specify what information expected?
      @initialize()
      @bindEvents()

    initialize: () ->
      $(@container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
        labels: @config.labels
      @createDownloadMenu() if not @edwareDownloadMenu
      @createAcademicYear() if not @academicYear

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

      # bind academic year info popover
      $('.academicYearInfoIcon').edwarePopover
        content: 'placeholder'

    createDownloadMenu: () ->
      @edwareDownloadMenu = new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config)

    createAcademicYear: () ->
      return if not @config.academicYears
      options = @config.academicYears.options
      callback = @config.academicYears.callback
      @academicYear ?= $('#academicYear').createYearDropdown options, callback

  create = (container, config) ->
    new ReportInfoBar(container, config)

  ReportInfoBar: ReportInfoBar
  create: create
