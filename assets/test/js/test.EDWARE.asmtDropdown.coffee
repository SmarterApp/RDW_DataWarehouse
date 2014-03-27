define ["jquery", "edwareAsmtDropdown", "edwarePreferences"], ($, edwareAsmtDropdown, edwarePreferences) ->

  EdwareAsmtDropdown = edwareAsmtDropdown.EdwareAsmtDropdown

  dropdownValues = [{asmtType: 'asmtType1', display: 'display1', value: 'value1'}, { asmtType: 'asmtType2', display: 'display2', value: 'value2'}]

  getPreference = ()->
    {}

  module "EDWARE.AsmtDropdown",
    setup: ->
      $("body").append "<div id='asmtDropdownContainer'></div>"

    teardown: ->
      $('#asmtDropdownContainer').remove()

  test "Test EdwareAsmtDropdown class", ->
    ok EdwareAsmtDropdown, "should have a EdwareAsmtDropdown class"
    equal typeof(EdwareAsmtDropdown), "function", "EdwareAsmtDropdown should be a class"

  test "Test EdwareAsmtDropdown jQuery plugin", ->
    ok $.fn.edwareAsmtDropdown, "jQuery should have a asmt dropdown plugin"

  test "Test EdwareAsmtDropdown initialization", ->
    edwarePreferences.saveAsmtPreference({ asmtType: 'asmtType2', display: 'display2', value: 'value2'})
    dropdown = new EdwareAsmtDropdown($('#asmtDropdownContainer'), dropdownValues, getPreference)
    ok $('.asmtTypeButton')[0], 'Should create an asmt type dropdown menu'
    equal $('#selectedAsmtType').text(), 'display1', 'Should select asmtType1 by default'

  test "Test selecting option", ->
    edwarePreferences.saveAsmtPreference({ asmtType: 'asmtType1', display: 'display1', value: 'value2'})
    dropdown = new EdwareAsmtDropdown $('#asmtDropdownContainer'), dropdownValues, getPreference, (asmtType) ->
      asmtType
    $('.asmtSelection[data-asmtType="asmtType1"]').click()
    equal $('#selectedAsmtType').text(), 'display1', 'Should set asmtType1 as display text'
