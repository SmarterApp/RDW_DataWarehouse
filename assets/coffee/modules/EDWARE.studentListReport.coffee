require [
  "edwareStudentList"
  "edwareFilter"
  "edwareDataProxy"
  "edwareConstants"
  "edwarePreferences"
], (edwareStudentList, edwareFilter, edwareDataProxy, Constants,
  edwarePreferences) ->

  reportName = Constants.REPORT_JSON_NAME.LOS

  edwareDataProxy.getDataForReport(reportName).done (config) ->
    studentGrid = new edwareStudentList.StudentGrid(config)
    # Add filter to the page
    edwareDataProxy.getDataForFilter().done (configs)->
      filter = $('#losFilter').edwareFilter '.filterItem', configs, (param)->
        asmt = edwarePreferences.getAsmtPreference()
        param.asmtType = asmt?.asmtType
        studentGrid.reload(param)
      filter.loadReport()
      filter.update {}
