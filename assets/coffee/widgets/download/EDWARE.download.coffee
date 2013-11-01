define [
  "jquery"
  "mustache"
  "text!CSVOptionsTemplate"
  "edwareConstants"
], ($, Mustache, CSVOptionsTemplate, Constants) ->

  ERROR_TEMPLATE = $(CSVOptionsTemplate).children('#ErrorMessageTemplate').html()

  SUCCESS_TEMPLATE = $(CSVOptionsTemplate).children('#SuccessMessageTemplate').html()
  
  class CSVDownloadModal
  
    constructor: (@container, @config) ->
      this.initialize()
      this.bindEvents()
      
    initialize: ()->
      this.container = $(this.container)
      output = Mustache.to_html CSVOptionsTemplate, {
        CSVOptions: this.config
      }
      this.container.html output
      this.message = $('#message', this.container)
      this.dropdownMenu = $('.dropdown-menu', this.container)

    bindEvents: ()->
      # prevent dropdown memu from disappearing
      $(this.dropdownMenu).click (e) ->
        e.stopPropagation()
      
      $('input:checkbox', this.container).click ()->
        $this = $(this)
        $dropdown = $this.closest('.btn-group')
        $display = $dropdown.find('span.dropdown-display')
        # get selected option text
        checked = []
        $dropdown.find('input:checked').each () ->
          checked.push $(this).data('label')
        $display.text checked.join(Constants.DELIMITOR.COMMA)

      self = this
      $('.btn-primary', this.container).click ()->
        self.sendRequest "/services/extract"

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