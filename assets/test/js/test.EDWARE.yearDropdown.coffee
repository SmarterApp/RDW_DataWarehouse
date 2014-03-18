define ["jquery", "edwareYearDropdown", "edwarePreferences"], ($, edwareYearDropdown, edwarePreferences) ->

  AcademicYearDropdown = edwareYearDropdown.AcademicYearDropdown

  dropdownValues = [2015, 2014]

  module "EDWARE.AcademicYearDropdown",
    setup: ->
      $("body").append "<div id='yearDropdownContainer'></div>"

    teardown: ->
      $('#yearDropdownContainer').remove()

  test "Test AcademicYearDropdown class", ->
    ok AcademicYearDropdown, "should have a AcademicYearDropdown class"
    equal typeof(AcademicYearDropdown), "function", "AcademicYearDropdown should be a class"

  test "Test AcademicYearDropdown jQuery plugin", ->
    ok $.fn.createYearDropdown, "jQuery should have a academic year dropdown plugin"
    widget = $('#yearDropdownContainer').createYearDropdown dropdownValues, ()->
      "callback value"
    ok widget, "jQuery plugin should create a year dropdown widget"

  test "Test AcademicYearDropdown initialization", ->
    edwarePreferences.saveAsmtYearPreference(2015)
    dropdown = new AcademicYearDropdown($('#yearDropdownContainer'), dropdownValues)
    ok $('.asmtYearButton')[0], 'Should create an asmt year dropdown menu'
    equal $('#selectedAcademicYear').text(), '2014 - 2015', 'Should select 2015 by default'

  test "Test selecting option", ->
    edwarePreferences.saveAsmtYearPreference(2015)
    dropdown = new AcademicYearDropdown $('#yearDropdownContainer'), dropdownValues, (year) ->
      year
    $('.asmtYearButton[data-value="2014"]').click()
    equal $('#selectedAcademicYear').text(), '2013 - 2014', 'Should set year 2014 as display text'
