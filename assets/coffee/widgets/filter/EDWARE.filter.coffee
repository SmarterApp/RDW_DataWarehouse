define [
  "jquery"
  "mustache"
  "bootstrap"
  "edwareDataProxy"
  "edwareUtil"
  "text!edwareFilterTemplate"
], ($, Mustache, bootstrap, edwareDataProxy, edwareUtil, filterTemplate) ->
  
  # * EDWARE filter widget
  # * The module contains EDWARE filter creation method
  FILTER_CLOSE = 'edware.filter.close'
  
  FILTER_SUBMIT = 'edware.filter.submit'
  
  RESET_DROPDOWN = 'edware.filter.reset.dropdown'
  
  class EdwareFilter
    
    constructor: (@filterArea, @filterTrigger, @callback) ->
      this.loadPage()
      this.initialize()
      # bind click event
      this.bindEvents()
      return this.filterArea
      
    initialize: ->
      # initialize variables
      this.filterArrow = $('.filterArrow', this.filterArea)
      this.filterPanel = $('.filter', this.filterArea)
      this.dropdownMenu = $('.dropdown-menu', this.filterArea)
      this.options = $('input', self.dropdownMenu)
      this.cancelButton = $('#cancel-btn', this.filterArea)
      this.submitButton = $('#submit-btn', this.filterArea)
      this.gradesFilter = $('.grade_range label input', this.filterPanel)
      this.filters = $('.filter-group', this.filterPanel)
      this.tagPanelWrapper = $('.selectedFilter_panel', this.filterArea)
      this.tagPanel = $('.filters', this.tagPanelWrapper)
      this.clearAllButton = $('.icon_removeAll', this.filterArea)

    loadPage: ->
      # load config from server
      config = this.loadConfig()
      output = Mustache.to_html filterTemplate, config
      $(this.filterArea).html output
    
    loadConfig: ->
      options =
        async: false
        method: "GET"
      
      config = {}
      edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
        config = data
      config
      
    bindEvents: ->
      self = this
      # subscribe filter close event
      this.filterArea.on FILTER_CLOSE, () ->
        self.closeFilter()
      
      # attach click event to cancel button
      this.cancelButton.click () ->
        self.closeFilter()
      
      # attach click event to submit button
      this.submitButton.click () ->
        $(self).trigger FILTER_SUBMIT
                
      # attach click event to filter trigger button
      this.filterTrigger.click ->
        self.toggleFilterArea self
        
      # toggle grades checkbox effect
      this.gradesFilter.click () ->
        $(this).parent().toggleClass('blue')
    
      # prevent dropdown memu from disappearing
      $(this.dropdownMenu).click (e) ->
          e.stopPropagation()
      
      $(this.filters).on RESET_DROPDOWN, this.clearOptions
       
      $(this).on FILTER_SUBMIT, self.submitFilter
      
      # attach click event to 'Clear All' button
      $(this.clearAllButton).click ->
        self.clearAll()
        
      # display user selected option on dropdown
      $(this.options).click ->
        self.showOptions $(this).closest('.btn-group')
        
    toggleFilterArea: (self) ->
      filterPanel = $(self.filterPanel)
      filterArrow = $(self.filterArrow)
      if filterPanel.is(':hidden')
         filterArrow.show()
         filterPanel.slideDown 'slow'
      else
         filterPanel.trigger FILTER_CLOSE
         
    closeFilter: ->
      this.filterPanel.slideUp 'slow'
      noTags = $(this.tagPanel).is(':empty')
      if noTags
        filterArrow = this.filterArrow
        this.tagPanelWrapper.slideUp 'slow', ->
          filterArrow.hide()
      else
        this.tagPanelWrapper.show()
        this.filterArrow.show()

    clearAll: ->
      # clear tag panel
      $(this.tagPanel).html("")
      # reset all filters
      this.filters.each () ->
        $(this).trigger RESET_DROPDOWN
      # trigger ajax call
      $(this).trigger FILTER_SUBMIT
  
    submitFilter: ->
      this.submitAjaxCall this.callback
      # display selected filters on html page
      this.createFilterBar this
      this.closeFilter()
    
    createFilterBar: ->
      self = this
      # remove existing filter labels
      this.tagPanel.empty()
      
      # create tags for selected filter options
      this.filters.each () ->
        tag = new EdwareFilterTag($(this), self)
        $(self.tagPanel).append tag.create() unless tag.isEmpty
    
    submitAjaxCall: (callback) ->
      selectedValues = this.getSelectedValues()
      # construct params and send ajax call
      params = edwareUtil.getUrlParams()
      # merge selected options into param
      $.extend(params, selectedValues)
      console.log params
      callback params if callback
      
    # get parameters for ajax call
    getSelectedValues: ->
      # get fields of selected options in json format
      params = {}
      $('.filter-group').each () ->
        paramName = $(this).data('name')
        paramValues = []
        $(this).find('input:checked').each () ->
          paramValues.push String($(this).data('value'))
        params[paramName] = paramValues if paramValues.length > 0
      params

    clearOptions: ->
      checkBox = $(this).find("input:checked")
      checkBox.attr("checked", false)
      checkBox.parent().toggleClass('blue')
      # reset dropdown component text
      $(this).find('.selected').remove()
    
    # show selected options on dropdown component
    showOptions: (buttonGroup) ->
      button = $('button', buttonGroup)
      text = this.getSelectedOptionText buttonGroup
      # remove existing text
      $('.selected', button).remove()
      # compute width property, subtract 20px for margin
      textLength = this.computeTextWidth button
      $('.display', button).append $('<div class="selected">').css('width', textLength).text(text)
      
    # get selected option text as string separated by comma
    getSelectedOptionText: (buttonGroup) ->
      delimiter = ', '
      text =  $('input:checked', buttonGroup).map(() ->
                    $(this).data('label')
              ).get().join(delimiter)
      if text isnt "" then '(' + text + ')'  else ""
    
    # compute width property for text
    computeTextWidth: (button) ->
      parseInt($(button).css('width')) - parseInt($('.display', button).css('width')) - 20



  class EdwareFilterTag
    
    constructor: (@dropdown, @filter) ->
      this.init()
      this.bindEvents()
    
    create: ->
      this.label
      
    init: ->
      param = {}
      param.display = this.dropdown.data('display')
      param.values = []
      this.dropdown.find('input:checked').each () ->
        param.values.push $(this).data('label')
      this.label = this.generateLabel param
      this.isEmpty = (param.values.length == 0)
      
    generateLabel: (data) ->
      template = "{{#.}}<div class='selectedFilterGroup'><div class='pull-left'><span>{{display}}: </span>{{#values}}<span>{{.}}</span> <span class='seperator'>, </span>{{/values}}</div><div class='removeIcon pull-left'></div></div>{{/.}}"
      output = Mustache.to_html(template, data)
      $(output)
      
    bindEvents: ->
      self = this
      # attach click event on remove icon
      $('.removeIcon', this.label).click () ->
        self.remove self
      
    # remove individual filters
    remove: (self) ->
      #remove label
      $(self.label).remove()
      # reset filter
      $(self.dropdown).trigger RESET_DROPDOWN
      # trigger ajax call
      $(self.filter).trigger FILTER_SUBMIT



  #
  #    *  EDWARE Filter plugin
  #    *  @param filterHook - Panel config data
  #    *  @param filterTrigger - 
  #    *  @param callback_func - callback function, triggered by click event on apply button
  #    *  Example: $("#table1").edwareGrid(columnItems, gridOptions)
  #  
  (($)->
    $.fn.edwareFilter = (filterTrigger, callback) ->
      new EdwareFilter($(this), filterTrigger, callback)
  ) jQuery
