require ["EDWARE.studentList", "edwareFilter", "edwareDataProxy", "edwareConstants"], (edwareStudentList, edwareFilter, edwareDataProxy, Constants) ->

  edwareDataProxy.getDataForReport(Constants.REPORT_JSON_NAME.LOS).done (config) ->
    studentGrid = new edwareStudentList.StudentGrid(config)
    # Add filter to the page
    edwareDataProxy.getDataForFilter().done (configs)->
      filter = $('#losFilter').edwareFilter '.filterItem', configs, (param)->
        studentGrid.reload(param)
      filter.loadReport()
      filter.update {}
