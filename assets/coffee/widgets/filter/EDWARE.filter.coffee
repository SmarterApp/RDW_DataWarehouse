define [
  "jquery"
  "mustache"
  "bootstrap"
  "text!edwareFilterTemplate"
], ($, Mustache, bootstrap, filterTemplate) ->
  
  # Generate a filter
  generateFilter = (filterHook, filterTrigger) ->
    output = Mustache.to_html filterTemplate
    $(filterHook).html(output)
    
    # bind click event
    bindEvent(filterTrigger, filterHook)
  
  bindEvent = (trigger, filterHook) ->
    $(trigger).click( () ->
       filterHook.toggle();
    )

  generateFilter: generateFilter