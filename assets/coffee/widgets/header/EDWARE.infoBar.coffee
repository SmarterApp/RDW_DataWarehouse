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
      @initialize()
      @bindEvents()

    initialize: () ->
      $(@container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
        labels: @config.labels
      years = getAcademicYears @config.academicYears.options
      @createDownloadMenu(years)
      @createAcademicYear(years)

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

    createDownloadMenu: (years) ->
      # merge academic years to JSON config
      @config.CSVOptions.asmtYear.options = years
      @edwareDownloadMenu ?= new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config)

    getAcademicYears = (years)->
      for year in years
        "display": toDisplay(year),
        "value": year

    toDisplay = (year)->
      (year - 1) + " - " + year

    createAcademicYear: (years) ->
      callback = @config.academicYears.callback
      @academicYear ?= $('#academicYear').createYearDropdown years, callback

  create = (container, config) ->
    new ReportInfoBar(container, config)

  ReportInfoBar: ReportInfoBar
  create: create
