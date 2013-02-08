#global define
define [
  "jquery"
  "cs!edwareUtil"
], ($, edwareUtil) ->
  
  #
  #    * Get Student data from the server
  #    * @param sourceURL - The student data API call
  #    * @param callback - callback function
  #    
  getDatafromSource = (sourceURL, params, callback) ->
    return false if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
    
    $.ajax(
      type: "POST"
      url: sourceURL
      data:
        JSON.stringify(params);
      dataType: "json"
      contentType: "application/json"
      success: (data) ->
        if callback
          callback data
        else
          data
      error: (xhr, ajaxOptions, thrownError) ->
        edwareUtil.displayErrorMessage xhr.status + ": " + thrownError
        #check401Error xhr.status
      )

  #
  #    * Get student list columns configuration
  # 
  getConfigs = (configURL, callback) ->
      return false if configURL is "undefined" or typeof configURL is "number" or typeof configURL is "function" or typeof configURL is "object"
        
      $.getJSON configURL, (data) ->
        studentsConfig = data.students
        
        if callback
           callback studentsConfig
        else
           studentsConfig
         
  check401Error = (status) ->
    location.href = "login.html?redirectURL=" + window.location.href if status is 401
        
  getDatafromSource: getDatafromSource
  getConfigs: getConfigs