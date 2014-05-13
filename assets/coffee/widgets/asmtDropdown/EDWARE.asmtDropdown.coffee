define [
  "jquery"
  "mustache"
  "text!AsmtDropdownTemplate"
  "edwarePreferences"
], ($, Mustache, AsmtDropdownTemplate, edwarePreferences) ->

  class EdwareAsmtDropdown

    constructor: (@container, @labels, @dropdownValues, @getAsmtPreference, @callback) ->
      @initialize()
      @setDefaultOption()
      @bindEvents()

    initialize: () ->
      for ddval in @dropdownValues
        ddval.asmt_grade = ddval.asmt_grade.replace('Grade', @labels.grade)
        if ddval.asmts isnt undefined
          for asmt in ddval.asmts
            asmt.asmt_subject_text = asmt.asmt_subject_text.replace('Details', @labels.details)
      @optionTemplate = @dropdownValues[0]?.display
      output = Mustache.to_html AsmtDropdownTemplate,
        dropdownValues: @dropdownValues
      @container.html(output)

    setDefaultOption: () ->
      # set default option, comment out for now
      asmt = @getAsmtPreference() #edwarePreferences.getAsmtPreference()
      if $.isEmptyObject(asmt)
        # set first option as default value
        asmt = @parseAsmtInfo $('.asmtSelection')
        edwarePreferences.saveAsmtPreference asmt
        edwarePreferences.saveAsmtForISR asmt
      if not asmt.subjectText
        asmt.subjectText = @dropdownValues[0]?.defaultSubjectText
      @setSelectedValue @getAsmtDisplayText(asmt)

    bindEvents: () ->
      self = this
      $('.asmtSelection', @container).click ->
        asmt = self.parseAsmtInfo $(this)
        subject = asmt.asmtView.split("_")
        # save subject value
        edwarePreferences.saveSubjectPreference subject
        displayText = self.getAsmtDisplayText(asmt)
        self.setSelectedValue displayText
        # additional parameters
        self.callback(asmt)
      $('.asmtSelection', @container).keypress event, ->
        if event.keyCode == 13 || event.keyCode == 32
          $(this).click()

    parseAsmtInfo: ($option) ->
      display: $option.data('display')
      asmtType: $option.data('asmttype')
      asmtGuid: $option.data('asmtguid')?.toString()
      asmtView: $option.data('value')
      effectiveDate: $option.data('effectivedate')
      effectiveDateText: $option.data('effectivedate-text')
      asmtGrade: $option.data('grade')
      subjectText: $option.data('subjecttext')

    setSelectedValue: (value) ->
      $('#selectedAsmtType').html value

    getAsmtDisplayText: (asmt)->
      Mustache.to_html @optionTemplate, asmt

  _format_effective_date = (effectiveDate) ->
    return "" if not effectiveDate
    effectiveDate = effectiveDate.toString()
    year = effectiveDate.substr(0, 4)
    month = effectiveDate.substr(4, 2)
    day = effectiveDate.substr(6, 2)
    "#{year}.#{month}.#{day}"

  # dropdownValues is an array of values to feed into dropdown
  (($)->
    $.fn.edwareAsmtDropdown = (labels, dropdownValues, getAsmtPreference, callback) ->
      for asmt in dropdownValues
        asmt.effective_date_text = _format_effective_date(asmt.effective_date)
      new EdwareAsmtDropdown($(this), labels, dropdownValues, getAsmtPreference, callback)
  ) jQuery

  EdwareAsmtDropdown: EdwareAsmtDropdown
