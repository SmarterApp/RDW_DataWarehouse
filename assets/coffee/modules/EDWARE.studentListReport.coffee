require ["../main"], (common) ->
  require ["EDWARE.studentList"], (edwareStudentList) ->
    getUrlParams = ->
      params = {}
      window.location.search.replace /[?&]+([^=&]+)=([^&]*)/g, (str, key, value) ->
        params[key] = value
    
      params
    params = getUrlParams()
    edwareStudentList.createStudentGrid params