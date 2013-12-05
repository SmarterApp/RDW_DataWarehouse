define [
  "jquery"
  "mustache"
], ($, Mustache) ->

  ASMT_TYPE_DROPDOWN_TEMPLATE =
    '<div class="btn-group">' +
      '<button type="button" class="btn btn-small dropdown-toggle" data-toggle="dropdown"><span id="selectedAsmtType">{{defaultValue}}</span></button>' +
      '<ul class="dropdown-menu" role="menu">' +
        '{{#dropdownValues}}<li class="asmtSelection" data-value="{{.}}"><a href="#">{{.}}</a></li>{{/dropdownValues}}' +
      '</ul>' +
    '</div>'

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
      selector = Mustache.to_html ASMT_TYPE_DROPDOWN_TEMPLATE, {
        defaultValue: defaultValue,
        dropdownValues: this.dropdownValues
      }
      this.dropdownSection.html(selector)

    setSelectedValue: (value) ->
      $('#selectedAsmtType').html value
      
  # dropdownValues is an array of values to feed into dropdown
  (($)->
    $.fn.edwareAsmtDropdown = (dropdownValues, callback) ->
      new EdwareAsmtDropdown($(this), dropdownValues, callback)
  ) jQuery
