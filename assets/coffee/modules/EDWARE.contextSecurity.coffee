define [
  'jquery'
  'bootstrap'
  'edwarePopover'
], ($, bootstrap, edwarePopover) ->

  DEFAULT_PERMISSIONS = {
    PII: {
      no_control: true,
      access_list: []
    },
    allow_assessment_extract: false,
    allow_registration_extract: true,
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
      return if @permissions.PII.no_control
      # bind tooltips popover
      $('a.disabled', '.ui-jqgrid').edwarePopover
        class: "no_pii_msg"
        placement: 'top'
        container: '#content'
        trigger: 'click'
        content: @no_pii_msg

    apply_raw_extract_security: () ->
      return if @permissions.allow_assessment_extract
      $('li.extract').hide()

    apply_bulk_extract_security: () ->
      assessment_access = @permissions.allow_assessment_extract
      registration_access = @permissions.allow_registration_extract
      # hide csv extract option if user doesn't have any permission
      if not assessment_access and not registration_access
        $('li.csv').hide()
      else if not assessment_access
        @remove_extractType('studentAssessment')
      else if not registration_access
        @remove_extractType('studentRegistrationStatistics')

    remove_extractType: (key) ->
      options = []
      for option in @extractType.options
        options.push option if option.value isnt key
      @extractType.options = options

    hasPIIAccess: (row_id) ->
      @permissions.PII.no_control or (row_id in @permissions.PII.access_list)


  init = (permissions, config) ->
    @security = new ContextSecurity(permissions, config)

  hasPIIAccess = (row_id) ->
    @security.hasPIIAccess(row_id)

  apply = () ->
    @security.apply()

  init: init
  apply: apply
  hasPIIAccess: hasPIIAccess
