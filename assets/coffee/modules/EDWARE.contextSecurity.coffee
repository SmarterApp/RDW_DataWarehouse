define [
  'jquery'
  'bootstrap'
  'edwarePopover'
], ($, bootstrap, edwarePopover) ->

  apply_pii_security = (user, no_pii_msg) ->
    return if user.allow_PII
    # remove links to next level
    $('a', '.ui-jqgrid').attr('href', '#').addClass('disabled').edwarePopover
      class: "no_pii_msg"
      placement: 'top'
      container: '#content'
      trigger: 'click'
      content: no_pii_msg

  apply_raw_extract_security = (user) ->
    return if user.allow_raw_extract
    $('li.extract').hide()

  apply_bulk_extract_security = (user, extractTypes) ->
    assessment_access = user.allow_assessment_extract
    registration_access = user.allow_registration_extract
    # hide csv extract option if user doesn't have any permission
    if not assessment_access and not registration_access
      $('li.csv').hide()
    else if not assessment_access
      remove_extractType('studentAssessment', extractTypes)
    else if not registration_access
      remove_extractType('studentRegistrationStatistics', extractTypes)

  remove_extractType = (key, extractType) ->
    options = []
    for option in extractType.options
      options.push option if option.value isnt key
    extractType.options = options

  apply = (user, config) ->
    apply_pii_security user, config.labels.no_pii
    apply_raw_extract_security user
    apply_bulk_extract_security user, config.CSVOptions.extractType


  apply: apply
  # below functions are exposed for unit testing
  apply_pii_security: apply_pii_security
  apply_raw_extract_security: apply_raw_extract_security
  apply_bulk_extract_security: apply_bulk_extract_security
