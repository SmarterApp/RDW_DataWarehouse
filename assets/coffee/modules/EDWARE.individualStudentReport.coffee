require ["EDWARE.individualStudent"], (edwareIndividualStudent) ->
  getUrlParams = ->
    params = {}
    window.location.search.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
      params[key] = value
  
    params
  
  params = getUrlParams()
  new edwareIndividualStudent.EdwareISR(params).load()
