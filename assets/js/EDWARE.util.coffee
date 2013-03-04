define [
  'jquery'
  'cs!EDWARE'
], ($, EDWARE) ->
  #
  # * EDWARE util
  # * Handles reusable or common methods required by other EDWARE javascript files
  # 
  
  #global EDWARE $ window 
    
  displayErrorMessage = (error) ->
    $("#errorMessage").html(error);
    
  getUrlParams = ->
    params = {}
    window.location.search.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
      params[key] = value
  
    params
    
    #
  #    * Get breadcrumbs data
  # 
  readJson = (templateURL, callback) ->
      return false if templateURL is "undefined" or typeof templateURL is "number" or typeof templateURL is "function" or typeof templateURL is "object"
        
      $.ajax
        url: templateURL
        dataType: "json"
        async: false
        success: (data) ->
          content = data

          if callback
            callback content
          else
            content
    
  displayErrorMessage: displayErrorMessage
  getUrlParams: getUrlParams
  readJson: readJson  
