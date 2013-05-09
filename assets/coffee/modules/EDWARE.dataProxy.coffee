#global define
define [
  "jquery"
  "edwareUtil"
  "edwareLoadingMask"
], ($, edwareUtil, edwareLoadingMask) ->
  
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
          location.href = "/assets/public/error.html"
      )          
         
  
  # Check 401 error
  check401Error = (status) ->
    location.href = "login.html?redirectURL=" + window.location.href if status is 401
        
  getDatafromSource: getDatafromSource