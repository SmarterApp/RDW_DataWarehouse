#global define
define [
  "jquery"
  "edwareUtil"
], ($, edwareUtil) ->

  @params = edwareUtil.getUrlParams()
  $("#dvSchoolName").html @params['schoolName']
  $("#spnGrade").html @params['grade']
  $("#spnPageCount").html @params['pageCount']
  if @params['pageCount'] == '1'
    $("#spnPages").html 'page'
  $("#spnStudentCount").html @params['studentCount']
  if @params['studentCount'] == '1'
    $("#spnStudents").html 'Student'
  $("#spnUserName").html @params['user']
  $("#spnDate").html @params['date']
  # For tenant level branding
  if @params['tenant_logo']
    element = $(".header .logo img")
    element.attr("src", "/assets/images/branding/" + @params['tenant_logo'])
    element.removeAttr("width")
    element.removeAttr("height")
  else if @params['gray']
    $(".header .logo img").attr("src", "../images/smarter_printlogo_gray.png")
