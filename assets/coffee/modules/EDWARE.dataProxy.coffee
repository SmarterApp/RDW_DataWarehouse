#global define
define [
  "jquery"
  "edwareUtil"
  "edwareLoadingMask"
  'edwareLanguage'
], ($, edwareUtil, edwareLoadingMask, i18n) ->
  
  #
  #    * Get data from the server via ajax call
  #    * @param sourceURL - The API call
  #    * @param options -  contains configs like method, async, data for "POST" etc.
  #    * @param callback - callback function
  #    
  getDatafromSource = (sourceURL, options, callback) ->
      
      return false  if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
      dataLoader = edwareLoadingMask.create(context: "<div></div>")
      dataLoader.show()
      
      $.ajax(
        type: options.method
        url: sourceURL
        async: options.async
        data:
          JSON.stringify(options.params) if options.params
        dataType: "json"
        contentType: "application/json"
        success: (data) ->
          dataLoader.remove()
          if callback
            callback data
          else
            data
        error: (xhr, ajaxOptions, thrownError) -> 
          dataLoader.remove()
          redirect_url = "/assets/public/error.html"
          # Read the redirect url on 401 Unauthorized Error
          if xhr.status == 401 and xhr.getResponseHeader('Content-Type').indexOf("application/json") != -1
            response = JSON.parse(xhr.responseText)
            redirect_url = response.redirect
          # Redirect the user to the appropriate url
          location.href = redirect_url
      )          
         
  getDataForReport = (reportName) ->
    language = i18n.getSelectedLanguage()
    json_url = ["../data/content/" + language + "/content.json", "../data/common/" + language + "/common.json",
      "../data/common/" + language + "/labels.json"]
    report_json_url = "../data/common/" + language + "/" + reportName + ".json"
    options =
        async: false
        method: "GET"
    idx = 0
    data = {}
    while idx < json_url.length
      getDatafromSource json_url[idx], options, (tmp_data)->
        $.extend data, tmp_data if typeof tmp_data is "object"
      idx++
    # merge legend
    getDatafromSource report_json_url, options, (tmp_data)->
      data['reportInfo'] = tmp_data['reportInfo']
      for key of tmp_data['legendInfo']
        data['legendInfo'][key] = tmp_data['legendInfo'][key] if tmp_data['legendInfo'].hasOwnProperty(key)
    # load messages resources
    getDatafromSource "../data/common/" + language + "/messages.json", options, (data) ->
      i18n.saveResources(data)
    data

  # Check 401 error
  check401Error = (status) ->
    location.href = "login.html?redirectURL=" + window.location.href if status is 401
        
  getDatafromSource: getDatafromSource
  getDataForReport: getDataForReport