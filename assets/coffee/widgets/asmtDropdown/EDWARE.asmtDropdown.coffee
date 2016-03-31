###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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

    # Ascending by date taken
    sortBy: (a, b) ->
      return if a.date_taken < b.date_taken then 1 else if a.date_taken > b.date_taken then -1 else 0

    getAsmtTypes: () ->
      reportName = this.config.reportName
      asmtTypes = {}
      @config.asmtTypes?.options.sort @sortBy
      for idx, asmt of @config.asmtTypes?.options
        asmt.asmt_year = asmt.date_taken.substr(0, 4) if asmt.date_taken
        asmt.asmt_type = Constants.ASMT_TYPE[asmt.asmt_type]
        asmt.display = @getAsmtDisplayText(asmt)
        key = if reportName is Constants.REPORT_NAME.ISR then asmt.asmt_type+asmt.asmt_period_year+asmt.date_taken else asmt.asmt_type
        asmtTypes[key] = (asmtTypes[key] || [])
        asmtTypes[key].push(asmt)
      asmtTypes

    setDefaultOption: () ->
      # set default option, comment out for now
      asmt = @getAsmtPreference()
      # For ISR, need also the grade
      matchAsmt = @dropdownValues[asmt.asmt_type+asmt.asmt_period_year+asmt.date_taken]
      asmt.asmt_grade = matchAsmt[0].asmt_grade if matchAsmt
      if $.isEmptyObject(asmt)
        # Dropdown blank w/o data
        # TODO|review years aval wo data
        return false if $('.asmtSelection').length is 0
        # set first option as default value
        asmt = @parseAsmtInfo $('.asmtSelection')
        edwarePreferences.saveAsmtPreference asmt
        if this.config.reportName is Constants.REPORT_NAME.ISR
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
      date_taken: $option.data('datetaken')
      asmt_grade: $option.attr('data-grade')
      asmt_period_year: $option.data('asmtperiodyear')

    setSelectedValue: (asmt) ->
      displayText = @getAsmtDisplayText(asmt, 'selection')
      $('#selectedAsmtType').html displayText

    getAsmtDisplayText: (asmt, option)->
      reportName = this.config.reportName
      #comparing_populations
      if reportName is Constants.REPORT_NAME.CPOP
        return "" if not asmt.date_taken
      #list_of_students
      if reportName is Constants.REPORT_NAME.LOS
        asmt.asmt_from_year = asmt.asmt_period_year - 1
        asmt.asmt_to_year = asmt.asmt_period_year
        option = 'preset' if not option
        return Mustache.to_html @displayTemplate[option], asmt
      #student report
      if reportName is Constants.REPORT_NAME.ISR
        asmt.asmt_from_year = asmt.asmt_period_year - 1
        asmt.asmt_to_year = asmt.asmt_period_year
        asmt.asmt_date = edwareUtil.formatDate(asmt.date_taken)
        return Mustache.to_html @displayTemplate[asmt.asmt_type], asmt

  # dropdownValues is an object to feed into the dropdown
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
