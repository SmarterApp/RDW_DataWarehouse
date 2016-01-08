require [
  'jquery'
  'edwareDataProxy'
  'edwareUtil'
], ($, edwareDataProxy, edwareUtil) ->
  
  goToLocation = (location) ->
     window.location.href = window.location.protocol + "//" + window.location.host + location
  
  if edwareUtil.isPublicReport()
    params = edwareUtil.getUrlParams()
    location = "/assets/html/comparingPopulations.html?isPublic=true&stateCode=" + params.stateCode
    goToLocation location
  else
    options =   
      method: 'POST'
    load = edwareDataProxy.getDatafromSource "/services/userinfo", options
    load.done (data) ->
      if edwareUtil.getDisplayBreadcrumbsHome data.user_info
        location = "/assets/html/stateMap.html" 
      else
        stateCode = edwareUtil.getUserStateCode data.user_info
        location = "/assets/html/comparingPopulations.html?stateCode=" + stateCode[0]
      goToLocation location

