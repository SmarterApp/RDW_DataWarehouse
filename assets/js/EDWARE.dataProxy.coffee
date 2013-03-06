#global define
define [
  "jquery"
  "cs!edwareUtil"
], ($, edwareUtil) ->
  
  #
  #    * Get data from the server via ajax call
  #    * @param sourceURL - The API call
  #    * @param options -  contains configs like method, async, data for "POST" etc.
  #    * @param callback - callback function
  #    
  getDatafromSource = (sourceURL, options, callback) ->
      
      $.ajax(
        type: options.method
        url: sourceURL
        async: options.async
        data:
          JSON.stringify(options.params) if options.params
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
         
  
  # Check 401 error
  check401Error = (status) ->
    location.href = "login.html?redirectURL=" + window.location.href if status is 401
        
  getDatafromSource: getDatafromSource