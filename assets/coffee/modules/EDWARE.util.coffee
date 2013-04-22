define [
  'jquery'
  'bootstrap'
], ($) ->
  #
  # * EDWARE util
  # * Handles constants, reusable or common methods required by other EDWARE javascript files
  # 
  
  #global $ window 
  
  constants = 
      overall_ald: 250
      psychometric_characterLimits: 250
      policyContent_characterLimits: 250
      claims_characterLimits: 140
      
  getConstants = (value) ->
    constants[value]
      
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
    
  # Given an user_info object, return the uid
  getUid = (userInfo) ->
    userInfo._User__info.uid
    
  # truncate the content and add ellipsis "..." if content is more than character limits
  truncateContent = (content, characterLimits)->
    if content.length > characterLimits
      content = content.substr(0, characterLimits)
      
      # ignore characters after the last word
      content = content.substr(0, content.lastIndexOf(' ') + 1) + "..."
      
    content

  
  getConstants: getConstants
  displayErrorMessage: displayErrorMessage
  getUrlParams: getUrlParams 
  getRole: getRole
  getUserName: getUserName
  getUid: getUid
  truncateContent: truncateContent
