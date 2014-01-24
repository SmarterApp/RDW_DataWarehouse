require [
  'jquery'
  'edwareDataProxy'
  'edwareUtil'
], ($, edwareDataProxy, edwareUtil) ->
  
  options =   
    method: 'POST'
  load = edwareDataProxy.getDatafromSource "/services/userinfo", options
  load.done (data) ->
    stateCode = edwareUtil.getUserStateCode data.user_info
    window.location.href = window.location.protocol + "//" + window.location.host + "/assets/html/comparingPopulations.html?stateCode=" + stateCode
