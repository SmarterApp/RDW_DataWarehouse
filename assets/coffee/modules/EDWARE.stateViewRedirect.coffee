###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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

