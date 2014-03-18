define [
  "jquery"
  "mustache"
  "text!YearDropdownTemplate"
  "edwarePreferences"
], ($, Mustache, YearDropdownTemplate, edwarePreferences) ->

  class AcademicYearDropdown

    constructor: (@container, @years, @callback) ->
      @initialize()
      @setDefaultOption()
      @bindEvents()

    initialize: () ->
      output = Mustache.to_html YearDropdownTemplate,
        options: @years
      $(@container).html output

    setDefaultOption: () ->
      asmtYear = edwarePreferences.getAsmtYearPreference()
      if not asmtYear
        asmtYear = @years[0].value
        edwarePreferences.saveAsmtYearPreference(asmtYear)
      @setSelectedValue (asmtYear - 1) + " - " + asmtYear

    setSelectedValue: (year) ->
      $("#selectedAcademicYear").html(year)

    bindEvents: () ->
      self = this
      $('li', @container).click ->
        display = $(this).data('display')
        self.setSelectedValue display
        value = $(this).data('value')
        edwarePreferences.saveAsmtYearPreference(value)
        self.callback(value)


  (($) ->
    $.fn.createYearDropdown = (options, callback)->
      new AcademicYearDropdown(this, options, callback)
  ) jQuery

  AcademicYearDropdown: AcademicYearDropdown
