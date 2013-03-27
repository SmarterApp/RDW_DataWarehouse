require ["../main"], (common) ->
  require ["EDWARE.studentList", "edwareUtil"], (edwareStudentList, edwareUtil) ->
    params = edwareUtil.getUrlParams()
    edwareStudentList.createStudentGrid params