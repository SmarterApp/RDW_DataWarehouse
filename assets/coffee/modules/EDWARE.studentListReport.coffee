require [
  "edwareStudentList"
  "edwareDataProxy"
  "edwareConstants"
  "edwarePreferences"
  "edwareUtil"
], (edwareStudentList, edwareDataProxy, Constants, edwarePreferences, edwareUtil) ->

  reportName = Constants.REPORT_JSON_NAME.LOS

  # load LOS configuration data
  edwareDataProxy.getDataForReport(reportName).done (config) ->
    studentGrid = new edwareStudentList.StudentGrid(config)
    params = edwareUtil.getUrlParams()
    params = mergeWithPreference(params)
    studentGrid.reload params

    # Add filter to the page
    # edwareDataProxy.getDataForFilter().done (configs)->
    #   filter = $('#losFilter').edwareFilter '.filterItem', configs, (param)->
    #     param = mergeWithPreference(param)
    #     studentGrid.reload(param)
    #   filter.loadReport()
    #   filter.update {}

  mergeWithPreference = (params)->
    edwarePreferences.saveStateCode(params['stateCode'])
    asmtYear = edwarePreferences.getAsmtYearPreference()
    params['asmtYear'] = asmtYear if asmtYear
    asmt = edwarePreferences.getAsmtPreference()
    # save preference for ISR
    edwarePreferences.saveAsmtForISR(asmt)
    params.asmtType = asmt?.asmtType
    params
