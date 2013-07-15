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
    
    # bind cancel button
    $('.filter #cancel-btn').click( () ->
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
      $(this).parent().toggleClass('blue');
    )


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
    filterVal = {}
    filterVal["filters"] = []
    filtersValOptions = filterVal["filters"]

    o = {}
    $('.filter input:checked').each () ->
      params[$(this).val()] = 'true'
      
      
      item = {}
      value = {}
        
      item["display"] = $(this).data("display")
      item["name"] = $(this).data("name")
      item["options"] = []
      
      value["label"] = $(this).data("label")
      value["value"] = $(this).data("value")
      item["options"].push(value)
      
      filtersValOptions.push(item)
    console.log(filterVal)
    #console.log(params)
    
    selectedVal = $(".filter input").serializeFormJSON()
    console.log(selectedVal)
    
    
    generateSelectedFilterBar filterVal
    callback params if callback
    
  generateSelectedFilterBar = (obj) ->
    $(".selectedFilter_panel .filters").empty()
    template = "{{#filters}}<div class='{{name}} selectedFilterGroup'><span>{{display}}:</span>{{#options}}<span>{{label}}</span>{{/options}}</div>{{/filters}}"
      
    output = Mustache.to_html(template, obj);
    $(".selectedFilter_panel .filters").html(output)
    
  $.fn.serializeFormJSON = ->
    o = {}
    a = @serializeArray()
    $.each a, ->
      if o[@name]
        o[@name] = [o[@name]]  unless o[@name].push
        o[@name].push @value or ""
      else
        o[@name] = @value or ""
  
    o
    
  generateFilter: generateFilter
  registerCallback: registerCallback