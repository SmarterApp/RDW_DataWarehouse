define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
  "edwarePopover"
  "edwareYearDropdown"
  "edwareDataProxy"
  "edwareUtil"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload, edwarePopover, edwareYearDropdown, edwareDataProxy, edwareUtil) ->

  class ReportInfoBar

    constructor: (@container, @config) ->
      @initialize()
      @bindEvent()

    initialize: () ->
      $(@container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
        labels: @config.labels
      years = edwareUtil.getAcademicYears @config.academicYears?.options
      @createAcademicYear(years)
      @createDownloadMenu()
      @render()

    bindEvent: () ->
      self = @
      $('.downloadIcon').click ->
        # show download menu
        self.edwareDownloadMenu.show()

    render: () ->
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
      @edwareDownloadMenu ?= new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config)

    createAcademicYear: (years) ->
      return if not years
      callback = @config.academicYears.callback
      @academicYear ?= $('#academicYearAnchor').createYearDropdown years, callback

  create = (container, config) ->
    infoBar = new ReportInfoBar(container, config)


  ReportInfoBar: ReportInfoBar
  create: create
