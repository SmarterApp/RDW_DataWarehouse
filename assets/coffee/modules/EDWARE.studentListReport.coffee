require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy"], (edwareStudentList, edwareFilter, edwareDataProxy) ->

  studentGrid = new edwareStudentList.StudentGrid()
  # Add filter to the page
  filterPromise = edwareDataProxy.getDataForFilter()
  filterPromise.done (configs)->
    filter = $('#losFilter').edwareFilter '.filterItem', configs, (param)->
      studentGrid.reload(param)
    filter.loadReport()
    filter.update {}
