define [
  "jquery"
  "mustache"
  "text!AsmtDropdownTemplate"
  "edwarePreferences"
], ($, Mustache, AsmtDropdownTemplate, edwarePreferences) ->

  class EdwareAsmtDropdown

    constructor: (@container, @dropdownValues, @callback) ->
      @initialize()
      @setDefaultOption()
      @bindEvents()

    initialize: () ->
      output = Mustache.to_html AsmtDropdownTemplate,
        dropdownValues: @dropdownValues
      @container.html(output)

    setDefaultOption: () ->
      # set default option
      asmt = edwarePreferences.getAsmtPreference()
      if $.isEmptyObject(asmt)
        # set first option as default value
        asmt = @parseAsmtInfo $('.asmtSelection')
        edwarePreferences.saveAsmtPreference asmt
      @setSelectedValue asmt.display

    bindEvents: () ->
      self = this
      $('.asmtSelection', @container).click ->
        asmt = self.parseAsmtInfo $(this)
        subject = asmt.asmtView.split("_")
        # save subject value
        edwarePreferences.saveSubjectPreference subject
        # save assessment type
        edwarePreferences.saveAsmtPreference asmt
        self.setSelectedValue asmt.display
        # additional parameters
        self.callback()

    parseAsmtInfo: ($option) ->
      display: $option.data('display')
      asmtType: $option.data('asmttype')
      asmtGuid: $option.data('asmtguid')?.toString()
      asmtView: $option.data('value')

    setSelectedValue: (value) ->
      $('#selectedAsmtType').html value

  # dropdownValues is an array of values to feed into dropdown
  (($)->
    $.fn.edwareAsmtDropdown = (dropdownValues, callback) ->
      new EdwareAsmtDropdown($(this), dropdownValues, callback)
  ) jQuery

  EdwareAsmtDropdown: EdwareAsmtDropdown
