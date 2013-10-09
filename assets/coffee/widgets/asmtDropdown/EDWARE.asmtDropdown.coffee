define [
  "jquery"
], ($) ->

  class EdwareAsmtDropdown
    
    constructor: (@dropdownSection, @dropdownValues, @callback) ->
      this.bindEvents()
      this
      
    bindEvents: () ->
      self = this
      $(document).on 'click', '.asmtSelection', (e) ->
        e.preventDefault()
        $this = $(this)
        value = $this.data('value')
        $('#selectedAsmtType').html value
        self.callback value
        
    create: () ->
      # By default, summative is default value, unless it doesn't exist
      defaultValue = "Summative"
      if this.dropdownValues.indexOf("Summative") == -1
        defaultValue = this.dropdownValues[0]
      selector = '<span class="btn-group">' +
      '<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">' +
      '<span id="selectedAsmtType">' + defaultValue +
      '</span><span class="caret"></span></button>' +
      '<ul class="dropdown-menu" role="menu">'
      for value in this.dropdownValues
        selector += '<li class="asmtSelection" data-value="' + value + '"><a href="#">' + value + '</a></li>'
      selector += '</ul></span>'
      this.dropdownSection.html(selector)
      # Calls callback function with the default value
      this.callback defaultValue
      
  # dropdownValues is an array of values to feed into dropdown
  (($)->
    $.fn.edwareAsmtDropdown = (dropdownValues, callback) ->
      new EdwareAsmtDropdown($(this), dropdownValues, callback)
  ) jQuery
