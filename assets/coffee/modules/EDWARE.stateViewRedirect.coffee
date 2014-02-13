require [
  'jquery'
  'edwareDataProxy'
  'edwareUtil'
], ($, edwareDataProxy, edwareUtil) ->
  
  options =   
    method: 'POST'
  load = edwareDataProxy.getDatafromSource "/services/userinfo", options
  load.done (data) ->
    if edwareUtil.getDisplayBreadcrumbsHome data.user_info
      location = "/assets/html/stateMap.html" 
    else
      stateCode = edwareUtil.getUserStateCode data.user_info
      location = "/assets/html/comparingPopulations.html?stateCode=" + stateCode[0]
    window.location.href = window.location.protocol + "//" + window.location.host + location