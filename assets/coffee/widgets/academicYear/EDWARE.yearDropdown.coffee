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
        options: @getAcademicYears()
      $(@container).html output

    setDefaultOption: () ->
      asmtYear = edwarePreferences.getAsmtYearPreference()
      asmtYear ?= @years[0]
      @setSelectedValue asmtYear

    setSelectedValue: (year) ->
      $("#selectedAcademicYear").html @toDisplay(year)

    getAcademicYears: ()->
      for year in @years
        "display": @toDisplay(year),
        "value": year

    toDisplay: (year)->
      (year - 1) + " - " + year

    bindEvents: () ->
      self = this
      $('li', @container).click ->
        value = $(this).data('value')
        edwarePreferences.saveAsmtYearPreference(value)
        self.setSelectedValue value
        self.callback(value)


  (($) ->
    $.fn.createYearDropdown = (options, callback)->
      new AcademicYearDropdown(this, options, callback)
  ) jQuery

  AcademicYearDropdown: AcademicYearDropdown
