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
    $(trigger).click( () ->
       if $(filterHook).is(":hidden")
         $(filterHook).slideDown('slow')
       else
         $(filterHook).slideUp('slow')
    )
    
    # prevent dropdown memu from disappearing
    $('.dropdown-menu input, .dropdown-menu label').click( (e) ->
        e.stopPropagation();
    );
    
    # bind cancel button
    $('.filter #cancel-btn').click( () ->
      $(filterHook).slideUp('slow')
    )
    
    # bind submit buttom
    $('.filter #submit-btn').click( () ->
      submitEvent()
      # slide up filter popup
      $(filterHook).slideUp('slow')
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
    $('.filter input:checked').each () ->
      params[$(this).val()] = 'true'
    console.log(params)
    callback params if callback
    
  generateFilter: generateFilter
  registerCallback: registerCallback