define [
  'jquery'
], ($) ->
   
  #
  #    * Loading mask widget
  #    
  $.fn.loader = (message) ->
    message = message || "Loading..."
    this.addClass("loader").html("<div class='message'>" + message + "</div>").appendTo "body"

  create = (opts) ->
    context = opts.context or "<div></div>"
    $(context).loader opts.message
        
  create: create