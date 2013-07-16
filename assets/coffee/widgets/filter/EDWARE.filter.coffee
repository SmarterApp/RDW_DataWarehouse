define [
  "jquery"
  "mustache"
  "bootstrap"
  "edwareDataProxy"
  "edwareUtil"
  "text!edwareFilterTemplate"
], ($, Mustache, bootstrap, edwareDataProxy, edwareUtil, filterTemplate) ->
  
  callback = undefined
  
  # Generate a filter
  generateFilter = (filterHook, filterTrigger) ->
    config = fetchConfig()
    output = Mustache.to_html filterTemplate, config
    $(filterHook).html(output)
    # bind click event
    bindEvent(filterTrigger, filterHook)
    this

  registerCallback = (callback_func) ->
    callback = callback_func

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
      clearOptions()
    
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

  fetchConfig = () ->
    options =
      async: false
      method: "GET"
    
    config = {}
    edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
      config = data
    config

  submitEvent = () ->
    # construct params and send ajax call
    params = edwareUtil.getUrlParams()
    selectedValues = fetchSelectedValues 'name', 'value'
    # merge selected options into param
    $.extend(params, selectedValues)
    console.log params
    callback params if callback
    # display selected filters on html page
    displaySelectedLabels $(".selectedFilter_panel .filters")
    
  displaySelectedLabels = (filterPanel) ->
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
      # bind to remove event
      $('.removeIcon', label).click () ->
        removeFilter $(label), $(dropdown) 
      $(filterPanel).append(label) if param.values.length > 0
    $(".selectedFilter_panel").show()
  
  generateLabel = (data) ->
    template = "{{#.}}<div class='selectedFilterGroup'><div class='pull-left'><span>{{display}}: </span>{{#values}}<span>{{.}}</span> <span class='seperator'>, </span>{{/values}}</div><div class='removeIcon pull-left'></div></div>{{/.}}"
    output = Mustache.to_html(template, data)
    $(output)
    
  fetchSelectedValues = (keyField, valueField) ->
    # get fields of selected options in json format
    params = {}
    $('.filter .filter-group').each () ->
      paramName = $(this).data(keyField)
      paramValues = []
      $(this).find('input:checked').each () ->
        paramValues.push $(this).data(valueField)
      params[paramName] = paramValues if paramValues.length > 0
    params


  generateFilter: generateFilter
  registerCallback: registerCallback