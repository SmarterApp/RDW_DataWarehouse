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
      @container = $(@container)
      @container.html Mustache.to_html ActionBarTemplate,
        labels: @config.labels
      @legend ?= @createLegend()
      @asmtDropdown ?= @createAsmtDropdown()
      @printer ?= @createPrint()

    createPrint: () ->
      @printer = edwarePrint.create '.printModal'

    createLegend: () ->
      # create legend
      $('.legendPopup').createLegend @config.reportName,
        legendInfo: @config.legendInfo
        subject: @prepareSubjects()
        labels: @config.labels

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
      # use customized subject interval
      return @config.subject if @config.subject
      # use sample interval
      legendInfo = @config.legendInfo
      colorsData = @config.colorsData
      # merge default color data into sample intervals data
      for color, i in colorsData.subject1.colors || colorsData.subject2.colors || @config.colors
        legendInfo.sample_intervals.intervals[i].color = color
      legendInfo.sample_intervals

    bindEvents: () ->
      self = this
      # create legend popover
      $("li.legendItem").popover
        html: true
        placement: 'bottom'
        trigger: 'manual'
        content: $(".legendPopup").html()
        container: @container
        template: LEGEND_POPOVER_TEMPLATE
      .click (e) ->
        $this = $(this)
        $this.addClass('active').popover('show')
        # hide next sibling's divider
        siblingDivider = $this.nextAll('li:visible').first().find('.divider')
        siblingDivider.css('border-left-color', '#f4f4f4')
      .mouseleave (e)->
        $this = $(this)
        $this.removeClass('active')
        $this.popover('hide')
        # show next sibling's divider
        siblingDivider = $this.nextAll(':visible').first().find('.divider')
        siblingDivider.css('border-left-color', '#e2e2e2')
      .on 'shown.bs.popover', ->
        # center legend popover to prevent it overflow the screen
        offset = $(this).offset().left
        bodyOffset = self.container.offset().left
        $popover = $('.legendPopover')
        popoverOffset = bodyOffset + (self.container.width() - $popover.width()) / 2
        $popover.css "left", popoverOffset
        # update arrow
        arrow = $(".arrow", $popover)
        arrow.css "left", offset - popoverOffset + $(this).width() / 2

      # bind print popover
      $('span.printLabel').click ->
        self.printer.show()

  create = (container, config, reloadCallback) ->
    new ReportActionBar(container, config, reloadCallback)

  ReportActionBar: ReportActionBar
  create: create
