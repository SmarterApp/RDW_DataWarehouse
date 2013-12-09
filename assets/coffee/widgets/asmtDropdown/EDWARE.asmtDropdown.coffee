define [
  "jquery"
  "mustache"
  "text!AsmtDropdownTemplate"
  "edwarePreferences"
], ($, Mustache, AsmtDropdownTemplate, edwarePreferences) ->

  class EdwareAsmtDropdown
    
    constructor: (@container, @dropdownValues, @callback) ->
      @initialize()
      @bindEvents()
            
    initialize: () ->
      output = Mustache.to_html AsmtDropdownTemplate,
        dropdownValues: @dropdownValues
      @container.html(output)
      # set default option
      savedAsmtType = edwarePreferences.getAsmtPreference()
      defaultValue = $('li.asmtSelection[data-asmttype="' + savedAsmtType + '"]').data('display')
      @setSelectedValue defaultValue
      
    bindEvents: () ->
      self = this
      $('.asmtSelection', @container).click ->
        $this = $(this)
        display = $this.data('display')
        asmtType = $this.data('asmttype')
        subject = $this.data('value').split("_")
        # save subject value
        edwarePreferences.saveSubjectPreference subject
        # save assessment type
        edwarePreferences.saveAsmtPreference asmtType
        self.setSelectedValue display
        # additional parameters
        self.callback $this.data('value')

    setSelectedValue: (value) ->
      $('#selectedAsmtType').html value
      
  # dropdownValues is an array of values to feed into dropdown
  (($)->
    $.fn.edwareAsmtDropdown = (dropdownValues, callback) ->
      new EdwareAsmtDropdown($(this), dropdownValues, callback)
  ) jQuery
