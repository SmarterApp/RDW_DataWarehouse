#global define
define [
  "jquery"
  "edwareUtil"
], ($, edwareUtil) ->

  @params = edwareUtil.getUrlParams()
  $("#dvSchoolName").html @params['schoolName']
  $("#spnGrade").html @params['grade']
  $("#spnPageCount").html @params['pageCount']
  $("#spnStudentCount").html @params['studentCount']
  $("#spnUserName").html @params['user']
  $("#spnDate").html @params['date']
