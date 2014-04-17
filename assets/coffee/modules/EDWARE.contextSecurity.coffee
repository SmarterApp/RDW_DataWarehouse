define [
  'jquery'
  'bootstrap'
  'edwarePopover'
], ($, bootstrap, edwarePopover) ->

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

    constructor: (permissions, config) ->
      @permissions = $.extend(true, {}, DEFAULT_PERMISSIONS, permissions)
      @no_pii_msg = config.labels.no_pii
      @extractType = config.CSVOptions.extractType

    apply: () ->
      @apply_pii_security()
      @apply_raw_extract_security()
      @apply_bulk_extract_security()

    apply_pii_security: () ->
      return if @permissions.pii.all
      warningIcon = '<i class="edware-icon-warning"></i>'
      # bind tooltips popover
      $('a.disabled', '.ui-jqgrid').edwarePopover
        class: "no_pii_msg"
        placement: 'top'
        container: '#content'
        trigger: 'click'
        content: warningIcon + @no_pii_msg

    apply_raw_extract_security: () ->
      return if @permissions.sar_extracts.all
      $('li.extract').hide()

    apply_bulk_extract_security: () ->
      assessment_access = @permissions.sar_extracts.all
      registration_access = @permissions.srs_extracts.all
      completion_access = @permissions.src_extracts.all
      # hide csv extract option if user doesn't have any permission
      if not assessment_access and not registration_access and not completion_access
        $('li.csv').hide()
      if not assessment_access
        @remove_extractType('studentAssessment')
      if not registration_access
        @remove_extractType('studentRegistrationStatistics')
      if not completion_access
        @remove_extractType('studentRegistrationCompletion')

    remove_extractType: (key) ->
      options = []
      for option in @extractType.options
        options.push option if option.value isnt key
      @extractType.options = options

    hasPIIAccess: (row_id) ->
      @permissions.pii.all or (row_id in @permissions.pii.guid)


  init = (permissions, config) ->
    @security = new ContextSecurity(permissions, config)

  hasPIIAccess = (row_id) ->
    if not @security
      return true
    @security.hasPIIAccess(row_id)

  apply = () ->
    @security.apply()

  init: init
  apply: apply
  hasPIIAccess: hasPIIAccess
