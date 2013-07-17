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
  
  # callback function
  callback = undefined
  
  #
  #    *  EDWARE Filter plugin
  #    *  @param filterHook - Panel config data
  #    *  @param filterTrigger - 
  #    *  @param callback_func - callback function, triggered by click event on apply button
  #    *  Example: $("#table1").edwareGrid(columnItems, gridOptions)
  #  
    
  # Generate a filter
  createFilter = (filterHook, filterTrigger, callback_func) ->
    # register callback
    callback = callback_func
    # load config from server
    config = loadConfig()
    output = Mustache.to_html filterTemplate, config
    $(filterHook).html(output)
    # bind click event
    bindEvent(filterTrigger, filterHook)

  bindEvent = (trigger, filterHook) ->
    filterArrow = $(filterHook).find('.filterArrow')
    filterPanel = $(filterHook).find('.filter')
    $(trigger).click () ->
       if $(filterPanel).is(":hidden")
         $(filterArrow).show()
         $(filterPanel).slideDown('slow')
       else
         $(filterPanel).slideUp 'slow', () ->
          $(filterArrow).hide()
    
    # prevent dropdown memu from disappearing
    $('.dropdown-menu').click( (e) ->
        e.stopPropagation();
    );
    
    # bind cancel button
    $('.filter #cancel-btn').click () ->
      $(filterPanel).slideUp 'slow', () ->
          $(filterArrow).hide() if $(".filters").children().length <= 0
          clearOptions $(filterPanel)
    
    # bind submit buttom
    $('.filter #submit-btn').click( () ->
      submitEvent()
      # slide up filter popup
      $(filterPanel).slideUp('slow')
    )
    
    # toggle grades checkbox effect
    $('.grade_range label input').click( () ->
      $(this).parent().toggleClass('blue')
    )

    # remove all filters
    $(".removeAllFilters .icon_removeAll").click( () ->
      removeAllSelectedFilters()
      submitEvent()
    )
    
    # display user selected option on dropdown
    $('.dropdown-menu input', filterHook).click (e) ->
      showOptions $(this).closest('.btn-group')
      
  # show selected options on dropdown component
  showOptions = (buttonGroup) ->
    button = $('button', buttonGroup)
    text = getSelectedOptionText buttonGroup
    # remove existing text
    $('.selected', button).remove()
    # compute width property, subtract 20px for margin
    textLength = computeTextWidth button
    $('.display', button).append $('<div class="selected">').css('width', textLength).text(text)
    
  # get selected option text as string separated by comma
  getSelectedOptionText = (buttonGroup) ->
    delimiter = ', '
    text =  $('input:checked', buttonGroup).map(() ->
                  $(this).data('label')
            ).get().join(delimiter)
    if text isnt "" then '(' + text + ')'  else ""
  
  # compute width property for text
  computeTextWidth = (button) ->
    parseInt($(button).css('width')) - parseInt($('.display', button).css('width')) - 20
  
  # remove individual filters
  removeFilter  = (label, dropdown) ->
    #remove label
    $(label).remove()
    # reset filter
    clearOptions dropdown
    removeAllSelectedFilters() if $(".filters").children().length <= 0
    # ajax call
    submitEvent()
    
  removeAllSelectedFilters = ->
    $(".selectedFilter_panel").slideUp 'fast', () ->
      $(".filterArrow").hide() if $('.filter').is(":hidden")
    $(".selectedFilter_panel .filters").html("")
    clearOptions $('.filter .filter-group')
    
  clearOptions = (element)->
      checkBox = $(element).find("input:checked")
      checkBox.attr("checked", false)
      checkBox.parent().toggleClass('blue')
      # reset dropdown component text
      $(element).find('.selected').remove()

  loadConfig = () ->
    options =
      async: false
      method: "GET"
    
    config = {}
    edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
      config = data
    config

  submitEvent = () ->
    selectedValues = fetchSelectedValues()
    if $.isEmptyObject(selectedValues)
      $('.filter #cancel-btn').trigger('click')
    else
      # construct params and send ajax call
      params = edwareUtil.getUrlParams()
      # merge selected options into param
      $.extend(params, selectedValues)
      console.log params
      callback params if callback
      # display selected filters on html page
      createSelectedFilterPanel() 
      
    
  createSelectedFilterPanel = ->
    filterPanel = $(".selectedFilter_panel .filters")
    # remove existing filter labels
    $(filterPanel).empty()
    
    $('.filter .filter-group').each () ->
      dropdown = $(this)
      param = {}
      param.display = $(this).data('display')
      param.values = []
      $(this).find('input:checked').each () ->
        param.values.push $(this).data('label')
      label = generateLabel param
      # attach click event on remove icon
      $('.removeIcon', label).click () ->
        removeFilter $(label), $(dropdown) 
      $(filterPanel).append(label) if param.values.length > 0
    $(".selectedFilter_panel").show()
  
  generateLabel = (data) ->
    template = "{{#.}}<div class='selectedFilterGroup'><div class='pull-left'><span>{{display}}: </span>{{#values}}<span>{{.}}</span> <span class='seperator'>, </span>{{/values}}</div><div class='removeIcon pull-left'></div></div>{{/.}}"
    output = Mustache.to_html(template, data)
    $(output)
    
  # get parameters for ajax call
  fetchSelectedValues = ->
    # get fields of selected options in json format
    params = {}
    $('.filter .filter-group').each () ->
      paramName = $(this).data('name')
      paramValues = []
      $(this).find('input:checked').each () ->
        paramValues.push $(this).data('value')
      params[paramName] = paramValues if paramValues.length > 0
    params


  create: createFilter