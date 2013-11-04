define [
  "jquery"
  "mustache"
  "text!CSVOptionsTemplate"
  "edwareConstants"
], ($, Mustache, CSVOptionsTemplate, Constants) ->

  ERROR_TEMPLATE = $(CSVOptionsTemplate).children('#ErrorMessageTemplate').html()

  SUCCESS_TEMPLATE = $(CSVOptionsTemplate).children('#SuccessMessageTemplate').html()

  INDIVIDUAL_VALID_TEMPLATE = $(CSVOptionsTemplate).children('#IndividualValidationTemplate').html()

  COMBINED_VALID_TEMPLATE = $(CSVOptionsTemplate).children('#CombinedValidationTemplate').html()
  
  class CSVDownloadModal
  
    constructor: (@container, @config) ->
      this.initialize()
      this.bindEvents()
      
    initialize: ()->
      this.container = $(this.container)
      output = Mustache.to_html CSVOptionsTemplate, {
        extractType: this.config['extractType']
        asmtType: this.config['asmtType']
        subject: this.config['asmtSubject']
      }
      this.container.html output
      this.message = $('#message', this.container)
      this.dropdownMenu = $('ul.dropdown-menu, ul.checkbox-menu', this.container)
      this.submitBtn = $('.btn-primary', this.container)
      this.asmtTypeBox = $('div#asmtType', this.container)
      this.selectDefault()

    bindEvents: ()->
      self = this
      # prevent dropdown memu from disappearing
      $(this.dropdownMenu).click (e) ->
        e.stopPropagation()
      
      $('input:checkbox', this.container).click (e)->
        $this = $(this)
        $dropdown = $this.closest('.btn-group')
        # remove ealier error messages
        $('div.error', self.messages).remove()
        if not self.validate($dropdown)
          $dropdown.addClass('invalid')
          self.showNoneEmptyMessage $dropdown.data('option-name')
        else
          $dropdown.removeClass('invalid')

      this.submitBtn.click ()->
        # remove ealier error messages
        $('div.error', self.messages).remove()
        # validate each selection group
        invalidFields = []
        $('div.btn-group', self.container).each ()->
          $dropdown = $(this)
          if not self.validate($dropdown)
            $dropdown.addClass('invalid')
            invalidFields.push $dropdown.data('option-name')
        if invalidFields.length isnt 0
          self.showCombinedErrorMessage invalidFields
        else
          $(this).attr('disabled','disabled')
          self.sendRequest "/services/extract"

    validate: ($dropdown) ->
      # check selected options
      checked = this.getSelectedOptions $dropdown
      checked.length isnt 0

    getSelectedOptions: ($dropdown)->
      # get selected option text
      checked = []
      $dropdown.find('input:checked').each () ->
        checked.push $(this).data('label')
      checked
                
    selectDefault: ()->
      # check first option of each dropdown
      $('ul li:nth-child(1) input',this.container).each ()->
        $(this).trigger 'click'

    sendRequest: (url)->
      params = this.getParams()
      # send request to backend
      request = $.ajax url, {
        type: 'POST'
        data: JSON.stringify(params)
        dataType: 'json'
        contentType: "application/json"
      }
      request.done this.showSuccessMessage.bind(this)
      request.fail this.showFailureMessage.bind(this)

    showSuccessMessage: (response)->
      this.message.html Mustache.to_html SUCCESS_TEMPLATE, {
        response: response
      }

    showFailureMessage: (response)->
      errorMessage = Mustache.to_html ERROR_TEMPLATE, {
        response: response
      }
      this.message.append errorMessage
      this.asmtTypeBox.addClass('invalid')

    showNoneEmptyMessage: (optionName)->
      validationMsg = Mustache.to_html INDIVIDUAL_VALID_TEMPLATE, {
        optionName: optionName.toLowerCase()
      }
      this.message.append validationMsg

    showCombinedErrorMessage: (optionNames)->
      validationMsg = Mustache.to_html COMBINED_VALID_TEMPLATE, {
        optionNames: optionNames
      }
      this.message.append validationMsg
                
    getParams: ()->
      params = {}
      this.dropdownMenu.each (index, param)->
        $param = $(param)
        key = $param.data('key')
        params[key] = []
        $param.find('input:checked').each ()->
          params[key].push $(this).attr('value')
      params

    show: () ->
      $('#CSVModal').modal()
                
  create = (container, config)->
    new CSVDownloadModal $(container), config
  
  CSVDownloadModal: CSVDownloadModal
  create: create