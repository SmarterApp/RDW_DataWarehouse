define [
  "jquery"
  "mustache"
  "text!CSVOptionsTemplate"
  "edwareConstants"
], ($, Mustache, CSVOptionsTemplate, Constants) ->

  ERROR_TEMPLATE = $(CSVOptionsTemplate).children('#ErrorMessageTemplate').html()

  SUCCESS_TEMPLATE = $(CSVOptionsTemplate).children('#SuccessMessageTemplate').html()

  NONE_EMPTY_TEMPLATE = $(CSVOptionsTemplate).children('#NoneEmptyValidTemplate').html()
  
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
        valid = true
        # remove ealier error messages
        $('div.error', self.messages).remove()
        # validate each selection group
        $('div.btn-group', self.container).each ()->
          $dropdown = $(this)
          console.log $dropdown.data('option-name')
          if not self.validate($dropdown)
            $dropdown.addClass('invalid')
            self.showNoneEmptyMessage $dropdown.data('option-name')
            valid = false
        if valid
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

    showNoneEmptyMessage: (optionName)->
      validationMsg = Mustache.to_html NONE_EMPTY_TEMPLATE, {
        optionName: optionName
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
      console.log(params);
      params

    show: () ->
      $('#CSVModal').modal()
                
  create = (container, config)->
    new CSVDownloadModal $(container), config
  
  CSVDownloadModal: CSVDownloadModal
  create: create