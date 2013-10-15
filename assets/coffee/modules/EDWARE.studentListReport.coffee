require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy", "edwareUtil"], (edwareStudentList, edwareFilter, edwareDataProxy, edwareUtil) ->

  studentGrid = new edwareStudentList.StudentGrid()
  # Add filter to the page
  configs = {}

  ( () ->
    configs = edwareDataProxy.getDataForFilter()
    edwareUtil.reRenderBody configs.labels
  )()

  filter = $('#losFilter').edwareFilter $('.filter_label'), configs, (param)->
    studentGrid.reload(param)
    
  filter.loadReport()
  filter.update {}
