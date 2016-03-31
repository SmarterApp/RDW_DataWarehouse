###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

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
