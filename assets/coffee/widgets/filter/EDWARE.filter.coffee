define [
  "jquery"
  "mustache"
  "bootstrap"
  "edwareDataProxy"
  "edwareUtil"
  "text!edwareFilterTemplate"
], ($, Mustache, bootstrap, edwareDataProxy, edwareUtil, filterTemplate) ->
  
  callback = undefined
  
  mapping = {}
  
  # Generate a filter
  generateFilter = (filterHook, filterTrigger) ->
    config = fetchConfig()
    output = Mustache.to_html filterTemplate, config
    $(filterHook).html(output)
    filterPanel = $(filterHook).find('.filter')
    # bind click event
    bindEvent(filterTrigger, filterPanel)
    this

  registerCallback = (callback_func) ->
    callback = callback_func

  bindEvent = (trigger, filterPanel) ->
    $(trigger).click( () ->
       if $(filterPanel).is(":hidden")
         $(filterPanel).slideDown('slow')
       else
         $(filterPanel).slideUp('slow')
    )
    
    # prevent dropdown memu from disappearing
    $('.dropdown-menu').click( (e) ->
        e.stopPropagation();
    );
    
     # Uncheck/reset all checkboxes
    $('.filter #cancel-btn').click( () ->
      resetFilterForm()
      $(filterPanel).slideUp('slow')
    )
    
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
    )
    
    # remove individual filters
    $(document).on
        click: (e) ->
           $(this).parent().remove()
           removeAllSelectedFilters() if $(".filters").children().length <= 0
      , ".selectedFilterGroup .removeIcon"

  removeAllSelectedFilters = ->
    $(".selectedFilter_panel").css("display", "none")
    $(".selectedFilter_panel .filters").html("")
    resetFilterForm()
    
  resetFilterForm = ->
      checkBox = $('.filter .filter-group').find("input:checked")
      checkBox.attr("checked", false)
      checkBox.parent().toggleClass('blue');
      
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
    selectedLabels = fetchSelectedLabels 'display', 'label'
    console.log params
    generateSelectedFilterBar selectedLabels if selectedLabels.length > 0
    callback params if callback
    
  generateSelectedFilterBar = (obj) ->
    $(".selectedFilter_panel .filters").empty()
    template = "{{#.}}<div class='selectedFilterGroup' data-name={{name}}><div class='pull-left'><span>{{display}}: </span>{{#options}}<span>{{.}}</span> <span class='seperator'>, </span>{{/options}}</div><div class='removeIcon pull-left'></div></div>{{/.}}"
      
    output = Mustache.to_html(template, obj);
    $(".selectedFilter_panel .filters").html(output)
    $(".selectedFilter_panel").css("display", "block")
    
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
    
  fetchSelectedLabels = (nameField, labelField) ->
    labels = fetchSelectedValues nameField, labelField
    filterValue = for key, value of labels
      val = {}; val['display'] = key; val['options'] = value
      val if value.length > 0
    filterValue

  generateFilter: generateFilter
  registerCallback: registerCallback