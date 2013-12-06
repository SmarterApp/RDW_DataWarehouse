define [
  "jquery"
  "bootstrap"
  "mustache"
  "text!ActionBarTemplate"
  "edwareDownload"
  "edwareLegend"
  "edwareAsmtDropdown"
  "edwareDisclaimer"
  "edwarePreferences"
  "edwarePrint"
], ($, bootstrap, Mustache, ActionBarTemplate, edwareDownload, edwareLegend, edwareAsmtDropdown, edwareDisclaimer, edwarePreferences, edwarePrint) ->

  LEGEND_POPOVER_TEMPLATE = '<div class="popover legendPopover"><div class="arrow"></div><div class="popover-inner large"><div class="popover-content"><p></p></div></div></div>'

  class ReportActionBar

    constructor: (@container, @config, @reloadCallback) ->
      @initialize()
      @bindEvents()

    initialize: () ->
      $(@container).html Mustache.to_html ActionBarTemplate,
        labels: @config.labels
      @legend ?= @createLegend()
      @asmtDropdown ?= @createAsmtDropdown() # create assessment type dropdown list
      @printer ?= @createPrinter()

    createPrinter: () ->
      @printer = edwarePrint.create '.printModal'
    
    createLegend: () ->
      # create legend
      $('.legendPopup').createLegend @config.reportName,
        legendInfo: @config.legendInfo
        subject: @config.subject || @prepareSubjects()

    # Create assessment type dropdown
    createAsmtDropdown: () ->
      self = this
      asmtDropdown = $('.asmtDropdown').edwareAsmtDropdown @config.asmtTypes, (asmtType) ->
        self.updateDisclaimer()
        self.reloadCallback asmtType
      @createDisclaimer()
      asmtDropdown

    createDisclaimer: () ->
      @disclaimer = $('.disclaimerInfo').edwareDisclaimer @config.interimDisclaimer
      @updateDisclaimer()

    updateDisclaimer: () ->
      currentAsmtType = edwarePreferences.getAsmtPreference()
      @disclaimer.update currentAsmtType

    prepareSubjects: () ->
      legendInfo = @config.legendInfo
      colorsData = @config.colorsData
      # merge default color data into sample intervals data
      for color, i in colorsData.subject1 || colorsData.subject2
        legendInfo.sample_intervals.intervals[i].color = color
      legendInfo.sample_intervals

    bindEvents: () ->
      self = this
      # create legend popover
      $("li.legendItem").popover
        html: true
        placement: 'bottom'
        trigger: 'manual'
        content: $("li.legendItem .legendPopup").html()
        container: "#actionBar"
        template: LEGEND_POPOVER_TEMPLATE
      .click (e) ->
        $(this).addClass('active').popover('show')
      .mouseleave (e)->
        $(this).removeClass('active')
        $(this).popover('hide')
      # bind print popover
      $('div.printLabel').click ->
        self.printer.show()

  create = (container, config, reloadCallback) ->
    new ReportActionBar(container, config, reloadCallback)

  ReportActionBar: ReportActionBar
  create: create