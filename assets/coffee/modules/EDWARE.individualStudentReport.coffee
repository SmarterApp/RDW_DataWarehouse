require ["../main"], (common) ->
  require ["EDWARE.individualStudent", "edwareUtil"], (edwareIndividualStudent, edwareUtil) ->
    params = edwareUtil.getUrlParams()
    edwareIndividualStudent.generateIndividualStudentReport params

