require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy", "edwareUtil"], (edwareStudentList, edwareFilter, edwareDataProxy, edwareUtil) ->
    # Add filter to the page
  configs = {}

  ( () ->
    configs =edwareDataProxy.getDataForFilter()
    edwareUtil.reRenderBody configs.labels
  )()

  filter = $('#losFilter').edwareFilter $('.filter_label'), configs, edwareStudentList.createStudentGrid
  filter.loadReport()
