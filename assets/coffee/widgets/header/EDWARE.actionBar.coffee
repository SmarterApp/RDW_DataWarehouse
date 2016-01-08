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
  "edwareUtil"
  "edwareYearDropdown"
  "edwareQuickLinks"
], ($, bootstrap, Mustache, ActionBarTemplate, edwareDownload, edwareLegend, edwareAsmtDropdown, edwareDisclaimer, edwarePreferences, edwarePrint, edwarePopover, Constants, edwareUtil, edwareYearDropdown, edwareQuickLinks) ->

  class ReportActionBar

    constructor: (@container, @config, @isPublic, asmt_type) ->
      @asmtType = {asmt_type: asmt_type} if asmt_type isnt 'undefined'
      @initialize()
      @bindEvents()

    initialize: () ->
      @container = $(@container)
      @container.html Mustache.to_html ActionBarTemplate,
        labels: @config.labels
        detailsSelection: @createDetailSelection()
      @legend ?= @createLegend()
      @printer ?= @createPrint()
      years = edwareUtil.getAcademicYears @config.academicYears?.options
      create = if @config.disableQuickLinks? then not @config.disableQuickLinks else true
      @createQuickLinks() if create
      @createAcademicYear(years)
      @createAsmtDropdown(years)

    createQuickLinks: () ->
      $('#quickLinks').createEdwareQuickLinks()

    createDetailSelection: () ->
      asmt = edwarePreferences.getAsmtPreference()
      asmtType = asmt?.asmt_type || Constants.ASMT_TYPE.SUMMATIVE
      for i in @config.detailsSelection?[asmtType] || []
        @config.detailsButtons[i]

    createAcademicYear: (years) ->
      return if not years
      callback = @config.academicYears.callback
      @academicYear ?= $('#academicYearAnchor').createYearDropdown years, callback

    createPrint: () ->
      @printer = edwarePrint.create '.printModal', @config.labels

    createLegend: () ->
      # create legend
      $('.legendPopup').createLegend @config.reportName, @isPublic,
        legendInfo: @config.legendInfo
        subject: @prepareSubjects()
        labels: @config.labels

    # Create assessment type dropdown
    createAsmtDropdown: (years) ->
      self = this
      if @config.reportName is Constants.REPORT_NAME.ISR
        preference = edwarePreferences.getAsmtForISR
      else
        preference = edwarePreferences.getAsmtPreference
      # render academic years
      @config.years= years
      $('.asmtDropdown').edwareAsmtDropdown @config, preference,
        onAcademicYearSelected: (academicYear) ->
          self.config.academicYears.callback academicYear
        onAsmtTypeSelected: (asmt) ->
          # save assessment type
          self.updateDisclaimer asmt
          self.config.asmtTypes.callback asmt
      @createDisclaimer()

    createDisclaimer: () ->
      @disclaimer = $('.disclaimerInfo').edwareDisclaimer @config.interimDisclaimer
      @updateDisclaimer(@asmtType)

    updateDisclaimer: (asmtType) ->
      currentAsmtType = asmtType?.asmt_type || edwarePreferences.getAsmtType() || {}
      @disclaimer.update currentAsmtType

    prepareSubjects: () ->
      # use customized subject interval
      return @config.subject if @config.subject
      # use sample interval
      legendInfo = @config.legendInfo
      colorsData = @config.colorsData
      # merge default color data into sample intervals data
      sampleColor = colorsData?.subject1 || colorsData?.subject2 || {}
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

      $('.academicYearInfoIcon').click ->
        $(this).popover('show')

      # bind subject details selecting events
      $("li.detailsItem button").click ()->
        $this = $(this)
        $this.siblings("button").removeClass('selected')
        $this.addClass('selected')
        asmtView = $this.data('view')
        edwarePreferences.saveAsmtView(asmtView)
        self.config.switchView asmtView


  create = (container, config, isPublic, asmt_type) ->
    new ReportActionBar(container, config, isPublic, asmt_type)

  ReportActionBar: ReportActionBar
  create: create
