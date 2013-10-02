require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy", "edwareUtil"], (edwareStudentList, edwareFilter, edwareDataProxy, edwareUtil) ->
  studentGrid = new edwareStudentList.StudentGrid()
    # Add filter to the page
  configs = {}

  ( () ->
    configs =edwareDataProxy.getDataForFilter()
    # Append the content into the body to prevent seeing the pre-templated text on the html
    $('body').append($('#edwareLOSBody').html())
    edwareUtil.reRenderBody configs.labels
  )()

  filter = $('#losFilter').edwareFilter $('.filter_label'), configs, (param)->
    studentGrid.reload(param)
    
  filter.loadReport()
