require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy"], (edwareStudentList, edwareFilter, edwareDataProxy) ->
    # Add filter to the page
  configs = {}

  ( () ->
    options =
        async: false
        method: "GET"
      
      edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
        configs = data
  )()

  filter = $('#losFilter').edwareFilter $('.filter_label'), configs, edwareStudentList.createStudentGrid
  filter.loadReport()
