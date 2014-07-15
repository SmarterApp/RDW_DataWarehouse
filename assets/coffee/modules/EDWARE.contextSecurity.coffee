define [
  'jquery'
  'bootstrap'
  'edwarePopover'
  'edwareConstants'
], ($, bootstrap, edwarePopover, Constants) ->

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
      @apply_state_download_security()

    apply_pdf_security: () ->
      if (@reportType is Constants.REPORT_TYPE.GRADE or @reportType is Constants.REPORT_TYPE.SCHOOL)
        if not @permissions.pii.all
          set_no_permission_option_by_class('li.pdf')
      else
        set_disabled_option_by_class('li.pdf')

    apply_pii_security_on_grid: () ->
      return if @permissions.pii.all
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

    apply_state_download_security: () ->
      #TODO: update state-level extract permission
      registration_access = @permissions.srs_extracts.all
      completion_access = @permissions.src_extracts.all
      # hide csv extract option if user doesn't have any permission
      return if registration_access or completion_access
      $('li.stateExtract').hide()

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
