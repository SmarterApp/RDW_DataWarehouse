define [
  "jquery"
  "mustache"
  "text!AsmtDropdownTemplate"
  "edwarePreferences"
  "edwareEvents"
  "edwareConstants"
  "edwareUtil"
], ($, Mustache, AsmtDropdownTemplate, edwarePreferences, edwareEvents, Constants, edwareUtil) ->

  class EdwareAsmtDropdown

    constructor: (@container, @config, @getAsmtPreference, @callbacks) ->
      @displayTemplate = @config.asmtSelectorTemplate
      @dropdownValues = @getAsmtTypes()
      @initialize()
      @setDefaultOption()
      @bindEvents()

    initialize: () ->
      currentYear = edwarePreferences.getAsmtYearPreference()
      latestYear = []
      otherYears = []

      for x,y of @dropdownValues

        # always the first one
        v = y[0]
        if v.asmt_period_year is currentYear
            latestYear.push v
        else
            otherYears.push v

      years = []
      currentYears = []
      if @config.years
        for year in @config.years
          if year.value isnt currentYear
            years.push year
          else
            currentYears.push year

      output = Mustache.to_html AsmtDropdownTemplate,
        latestYear: latestYear
        otherYears: otherYears
        hasOtherYears: otherYears.length > 0
        academicYears: years
        hasOtherAcademicYears: years.length > 0
        currentYear: currentYears[0]
      @container.html(output)

    getAsmtTypes: () ->
      asmtTypes = {}
      for idx, asmt of @config.asmtTypes?.options
        asmt.asmt_year = asmt.date_taken.substr(0, 4) if asmt.date_taken
        asmt.asmt_type = Constants.ASMT_TYPE[asmt.asmt_type]
        asmt.display = @getAsmtDisplayText(asmt)
        asmtTypes[asmt.asmt_type] = (asmtTypes[asmt.asmt_type] || [])
        asmtTypes[asmt.asmt_type].push(asmt)
      asmtTypes

    setDefaultOption: () ->
      # set default option, comment out for now
      asmt = @getAsmtPreference() #edwarePreferences.getAsmtPreference()
      if $.isEmptyObject(asmt)
        # set first option as default value
        asmt = @parseAsmtInfo $('.asmtSelection')
        edwarePreferences.saveAsmtPreference asmt
        edwarePreferences.saveAsmtForISR asmt
      @setSelectedValue asmt

    bindEvents: () ->
      self = this
      $(@container).onClickAndEnterKey '.asmtSelection', ->
        asmt = self.parseAsmtInfo $(this)
        self.setSelectedValue asmt
        # additional parameters
        self.callbacks.onAsmtTypeSelected(asmt)

      $(@container).onClickAndEnterKey '.asmtYearButton', ->
        value = $(this).data('value')
        edwarePreferences.saveAsmtYearPreference(value)
        self.callbacks.onAcademicYearSelected value

      # collapse dropdown menu when focus out
      $('.btn-group', @container).focuslost ->
        $(this).removeClass('open')

    parseAsmtInfo: ($option) ->
      display: $option.data('display')
      asmt_type: $option.data('asmttype')
      asmt_guid: $option.data('asmtguid')?.toString()
      effective_date: $option.data('effectivedate')
      date_taken: $option.data('datetaken')
      asmt_grade: $option.data('grade')
      asmt_period_year: $option.data('asmtperiodyear')

    setSelectedValue: (asmt) ->
      displayText = @getAsmtDisplayText(asmt)
      $('#selectedAsmtType').html displayText
      # show iab message
      $IABMessage =  $(".IABMessage")
      grade = @config.grade
      if asmt?.asmt_type is Constants.ASMT_TYPE.IAB and grade
        $('.grade', ".IABMessage").html grade?.id
        asmtView = edwarePreferences.getAsmtView()
        if not asmtView or asmtView is Constants.ASMT_VIEW.OVERVIEW
          edwarePreferences.saveAsmtView Constants.ASMT_VIEW.MATH
        $IABMessage.show()
      else
        $IABMessage.hide()

    getAsmtDisplayText: (asmt)->
      reportName = this.config.reportName
      #comparing_populations
      if reportName == Constants.REPORT_NAME.CPOP
        return "" if not asmt.effective_date
      #list_of_students
      if reportName == Constants.REPORT_NAME.LOS
        asmt.asmt_from_year = asmt.asmt_period_year - 1
        asmt.asmt_to_year = asmt.asmt_period_year
        return Mustache.to_html @displayTemplate.selection, asmt
      #student report
      if reportName == Constants.REPORT_NAME.ISR
        asmt.asmt_date = edwareUtil.formatDate(asmt.date_taken)
        return Mustache.to_html @displayTemplate.default, asmt

  # dropdownValues is an array of values to feed into dropdown
  (($)->
    $.fn.edwareAsmtDropdown = (config, getAsmtPreference, callbacks) ->
      # Check if only IAB is loaded for 1st time
      firstTimeLoad = if Object.keys(getAsmtPreference()).length == 0 then true else false
      new EdwareAsmtDropdown($(this), config, getAsmtPreference, callbacks)
      asmt = getAsmtPreference()
      if firstTimeLoad and asmt?.asmt_type == 'Interim Assessment Blocks'
        location.reload()
  ) jQuery

  EdwareAsmtDropdown: EdwareAsmtDropdown
