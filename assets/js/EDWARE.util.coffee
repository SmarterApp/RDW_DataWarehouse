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
    
  displayErrorMessage: displayErrorMessage
  getUrlParams: getUrlParams