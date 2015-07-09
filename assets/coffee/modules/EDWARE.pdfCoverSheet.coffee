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
  $("#spnReportCount").html @params['reportCount']
  if @params['reportCount'] == '1'
    $("#spnReports").html 'Report'
  $("#spnUserName").html @params['user']
  $("#spnDate").html @params['date']
  # For tenant level branding
  data = edwareUtil.getTenantBrandingDataForPrint {'branding': {'image': @params['tenant_logo']}}, @params['gray']
  $(".header .logo img").attr("src", data.tenantLogo)
