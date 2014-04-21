define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!InfoBarTemplate"
  "edwareDownload"
  "edwarePopover"
  "edwareYearDropdown"
  "edwareDataProxy"
], ($, bootstrap, Mustache, InfoBarTemplate, edwareDownload, edwarePopover, edwareYearDropdown, edwareDataProxy) ->

  class ReportInfoBar

    constructor: (@container, @config) ->
      @initialize()
      @bindEvent()

    initialize: () ->
      $(@container).html Mustache.to_html InfoBarTemplate,
        title: @config.reportTitle
        subjects: @config.subjects
        labels: @config.labels
      years = getAcademicYears @config.academicYears?.options
      @createAcademicYear(years)

    bindEvent: () ->
      self = @
      $('.downloadIcon').click ->
        loadingData = fetchData self.config.param
        loadingData.done (data)->
          self.render(data)

    render: (data) ->
      self = this
      # show download menu
      @createDownloadMenu(data)
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

    createDownloadMenu: (data) ->
      # merge academic years to JSON config
      years = getAcademicYears data.asmt_period_year
      studentRegYears = getAcademicYears data.studentRegAcademicYear
      @config.CSVOptions.asmtYear.options = years if years
      @config.CSVOptions.academicYear.options = years if years
      @config.CSVOptions.studentRegAcademicYear.options = studentRegYears if studentRegYears
      @edwareDownloadMenu ?= new edwareDownload.DownloadMenu($('#downloadMenuPopup'), @config)

    getAcademicYears = (years)->
      return if not years
      for year in years
        "display": toDisplay(year),
        "value": year

    toDisplay = (year)->
      (year - 1) + " - " + year

    createAcademicYear: (years) ->
      return if not years
      callback = @config.academicYears.callback
      @academicYear ?= $('#academicYearAnchor').createYearDropdown years, callback

    fetchData = (params)->
        options =
          method: "POST"
          params: params
        edwareDataProxy.getDatafromSource "/data/academic_year", options

  create = (container, config) ->
    infoBar = new ReportInfoBar(container, config)
    

  ReportInfoBar: ReportInfoBar
  create: create
