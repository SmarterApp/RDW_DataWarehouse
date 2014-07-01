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
  "edwarePopover"
  "edwareConstants"
  "edwareSearch"
], ($, bootstrap, Mustache, ActionBarTemplate, edwareDownload, edwareLegend, edwareAsmtDropdown, edwareDisclaimer, edwarePreferences, edwarePrint, edwarePopover, Constants, edwareSearch) ->

  class ReportActionBar

    constructor: (@container, @config, createSearch, @reloadCallback) ->
      @initialize(createSearch)
      @bindEvents()

    initialize: (createSearch) ->
      @container = $(@container)
      @container.html Mustache.to_html ActionBarTemplate,
        labels: @config.labels
      @legend ?= @createLegend()
      @asmtDropdown = @createAsmtDropdown()
      @printer ?= @createPrint()
      # Create search box if true, else remove it
      @searchBox ?= @createSearchBox() if createSearch 

    createSearchBox: () ->
      $('#search').edwareSearchBox @config.labels

    createPrint: () ->
      @printer = edwarePrint.create '.printModal', @config.labels

    createLegend: () ->
      # create legend
      $('.legendPopup').createLegend @config.reportName,
        legendInfo: @config.legendInfo
        subject: @prepareSubjects()
        labels: @config.labels

    # Create assessment type dropdown
    createAsmtDropdown: () ->
      if not @config.asmtTypes || @config.asmtTypes.length is 0
        $('.asmtTypeItem').remove()
        return
      self = this
      if @config.reportName is Constants.REPORT_NAME.ISR
        preference = edwarePreferences.getAsmtForISR
      else
        preference = edwarePreferences.getAsmtPreference
      asmtDropdown = $('.asmtDropdown').edwareAsmtDropdown @config.labels, @config.asmtTypes, preference, (asmt) ->
        self.updateDisclaimer asmt
        self.reloadCallback asmt
      @createDisclaimer()
      asmtDropdown

    createDisclaimer: () ->
      @disclaimer = $('.disclaimerInfo').edwareDisclaimer @config.interimDisclaimer
      @updateDisclaimer()

    updateDisclaimer: (asmtType) ->
      currentAsmtType = asmtType || edwarePreferences.getAsmtPreference()
      @disclaimer.update currentAsmtType

    update: () ->
      # Callback to search box to highlight if necessary
      @searchBox.addHighlight() if @searchBox

    prepareSubjects: () ->
      # use customized subject interval
      return @config.subject if @config.subject
      # use sample interval
      legendInfo = @config.legendInfo
      colorsData = @config.colorsData
      # merge default color data into sample intervals data
      sampleColor = colorsData.subject1 || colorsData.subject2
      for color, i in sampleColor.colors || @config.colors
        legendInfo.sample_intervals.intervals[i].color = color
      legendInfo.sample_intervals

    bindEvents: () ->
      self = this
      # create legend popover
      $("li.legendItem").edwarePopover
        class: "legendPopover"
        trigger: 'manual'
        content: $(".legendPopup").html()
      .click (e) ->
        $this = $(this)
        $this.addClass('active').popover('show')
        # hide next sibling's divider
        siblingDivider = $this.nextAll('li:visible').first().find('.divider')
        siblingDivider.css('border-left-color', '#f4f4f4')
      .on 'hidden.bs.popover', (e)->
        $this = $(this)
        $this.removeClass('active')
        # show next sibling's divider
        siblingDivider = $this.nextAll(':visible').first().find('.divider')
        siblingDivider.css('border-left-color', '#e2e2e2')

      # bind print popover
      $('a.printLabel').click ->
        self.printer.show()

  create = (container, config, createSearch, reloadCallback) ->
    new ReportActionBar(container, config, createSearch, reloadCallback)

  ReportActionBar: ReportActionBar
  create: create
