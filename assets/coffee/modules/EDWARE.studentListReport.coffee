require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy"], (edwareStudentList, edwareFilter, edwareDataProxy) ->

  studentGrid = new edwareStudentList.StudentGrid()
  # Add filter to the page
  configs = {}

  ( () ->
    configs = edwareDataProxy.getDataForFilter()
  )()

  filter = $('#losFilter').edwareFilter $('.filter_label'), configs, (param)->
    studentGrid.reload(param)
    
  filter.loadReport()
  filter.update {}
