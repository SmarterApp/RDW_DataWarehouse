define [
  "jquery"
  "mustache"
  "bootstrap"
   "edwareDataProxy"
  "text!edwareFilterTemplate"
], ($, Mustache, bootstrap, edwareDataProxy, filterTemplate) ->
  
  # Generate a filter
  generateFilter = (filterHook, filterTrigger) ->
    config = fetchConfig()
    output = Mustache.to_html filterTemplate, config
    $(filterHook).html(output)
    
    # bind click event
    bindEvent(filterTrigger, filterHook)


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


  fetchConfig = () ->
    options =
      async: false
      method: "GET"
    
    config = {}
    edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
      config = data
    config


  generateFilter: generateFilter