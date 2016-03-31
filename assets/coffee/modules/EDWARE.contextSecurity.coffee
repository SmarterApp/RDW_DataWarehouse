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

define [
  'jquery'
  'bootstrap'
  'edwareUtil'
  'edwarePopover'
  'edwareConstants'
], ($, bootstrap, edwareUtil, edwarePopover, Constants) ->

  DEFAULT_PERMISSIONS = {
    pii: {
      all: true,
      guid: []
    },
    sar_extracts: {
      all: true,
      guid: []
    },
    srs_extracts: {
      all: true,
      guid: []
    },
    src_extracts: {
      all: true,
      guid: []
    }
  }

  class ContextSecurity

    constructor: (permissions, config, @reportType) ->
      @permissions = $.extend(true, {}, DEFAULT_PERMISSIONS, permissions)
      @no_pii_msg = config.labels.no_pii
      @extractType = config.CSVOptions.extractType
      @isDistrict = @reportType is 'district'

    apply: () ->
      @apply_pii_security_on_grid()
      @apply_sar_security()
      @apply_pdf_security()
      @apply_state_security()

    apply_pdf_security: () ->
      if (@reportType is Constants.REPORT_TYPE.GRADE or @reportType is Constants.REPORT_TYPE.SCHOOL)
        if not @permissions.pii.all
          set_no_permission_option_by_class('li.pdf')
      else
        set_disabled_option_by_class('li.pdf')

    apply_pii_security_on_grid: () ->
      return if @permissions.pii.all
      # don't show warning for public report
      if not edwareUtil.isPublicReport()
        warningIcon = '<i class="edware-icon-warning"></i>'
        # bind tooltips popover
        $('a.disabled', '.ui-jqgrid').edwarePopover
          class: "no_pii_msg"
          placement: 'top'
          container: '#content'
          trigger: 'click'
          content: warningIcon + @no_pii_msg

    apply_sar_security: () ->
      return if @permissions.sar_extracts.all
      set_no_permission_option_by_class('li.extract')

    apply_state_security: () ->
      registration_access = @permissions.srs_extracts.all
      completion_access = @permissions.src_extracts.all
      audit_xml_access = @permissions.audit_xml_extracts.all
      item_lvl_access = @permissions.item_extracts.all
      if not (registration_access or completion_access or audit_xml_access or item_lvl_access)
        # hide State extract option if user doesn't have any permission
        $('li.stateExtract').hide()
      else
        # disable individual radio buttons
        if not registration_access
          set_disabled_option_by_class('.extractType li#registrationStatistics')
        if not completion_access
          set_disabled_option_by_class('.extractType li#completionStatistics')
        if not audit_xml_access
          set_disabled_option_by_class('.extractType li#rawXML')
        if not item_lvl_access
          set_disabled_option_by_class('.extractType li#itemLevel')

    hasPIIAccess: (row_id) ->
      @permissions.pii.all or (row_id in @permissions.pii.guid)


  init = (permissions, config, reportType) ->
    @security = new ContextSecurity(permissions, config, reportType)

  hasPIIAccess = (row_id) ->
    if not @security
      return true
    @security.hasPIIAccess(row_id)

  apply = () ->
    @security.apply()

  set_disabled_option_by_class = (classSelector) ->
    add_option_by_class(classSelector, 'disabled')

  set_no_permission_option_by_class = (classSelector) ->
    add_option_by_class(classSelector, 'noPermission')

  add_option_by_class = (classSelector, className) ->
    $(classSelector).addClass(className).find('input').attr('disabled', 'disabled')

  init: init
  apply: apply
  hasPIIAccess: hasPIIAccess
