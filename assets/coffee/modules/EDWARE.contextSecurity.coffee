define [
    'jquery'
], ($) ->

  apply_pii_security = (user, no_pii_msg) ->
    pii = true
    return if pii
    # remove links to next level
    $('a', '.ui-jqgrid').attr('href', '#').addClass('disabled').edwarePopover
      class: "no_pii_msg"
      placement: 'top'
      container: '#content'
      trigger: 'click'
      content: no_pii_msg

  apply_extract_security = (user) ->
    allow_extract = true
    return if allow_extract
    $('li.extract').hide()

  apply = (user, labels) ->
    apply_pii_security user, labels.no_pii
    apply_extract_security user


  apply: apply
