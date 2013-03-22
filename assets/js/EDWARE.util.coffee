define [
  'jquery'
], ($) ->
  #
  # * EDWARE util
  # * Handles reusable or common methods required by other EDWARE javascript files
  # 
  
  #global $ window 
    
  displayErrorMessage = (error) ->
    $("#errorMessage").html(error);
    
  getUrlParams = ->
    params = {}
    window.location.search.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
      params[key] = value
  
    params
  
  # Given an user_info object, return the one role of that user from the list
  getRole = (userInfo) ->
    # roles is a list, for beta, we can assume we only have 1 role
    userInfo._User__info.roles[0].toUpperCase()
  
  # Given an user_info object, return the first and last name of the user
  getUserName = (userInfo) ->
    userInfo._User__info.name.firstName + ' ' + userInfo._User__info.name.lastName

  displayErrorMessage: displayErrorMessage
  getUrlParams: getUrlParams 
  getRole: getRole
  getUserName: getUserName
