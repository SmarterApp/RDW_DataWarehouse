define [
  "jquery"
  "edwareContextSecurity"
], ($, contextSecurity) ->

  test_user =
    "allow_PII": true
    "allow_raw_extract": true
    "allow_assessment_extract": true
    "allow_registration_extract": true

  no_pii_msg = "No PII available"

  extractType = {
    options: [{
      value: "studentAssessment"
    }, {
      value: "studentRegistrationStatistics"
    }]
  }

  config = {
    labels: {no_pii: no_pii_msg},
    CSVOptions: {
      "extractType": extractType
    }
  }

  module "EDWARE.contextSecurity",
      setup: ->
        $("body").append "<div id='container'>
          <div id='header'></div>
          <div id='downloadMenuPopup'><li class='extract'></li><li class='csv'></li></div>
          <div id='content' class='ui-jqgrid'><a href='test.html'></a></div>
        </div>"

      teardown: ->
        $('#container').remove()

  test "Test context security module", ->
    ok contextSecurity, "contextSecurity should be a module"
    equal typeof(contextSecurity.apply), "function", "ContextSecurity.apply() should be a function"
    equal typeof(contextSecurity.apply_pii_security), "function", "ContextSecurity.apply_pii_security() should be a function"
    equal typeof(contextSecurity.apply_raw_extract_security), "function", "ContextSecurity.apply_raw_extract_security() should be a function"
    equal typeof(contextSecurity.apply_bulk_extract_security), "function", "apply_bulk_extract_security() should be a function"

  test "Test no pii", ->
    $anchor = $('a', '#content')
    test_user.allow_PII = true
    contextSecurity.apply_pii_security test_user, no_pii_msg
    equal $anchor.attr('href'), 'test.html'
    test_user.allow_PII = false
    contextSecurity.apply_pii_security test_user, no_pii_msg
    equal $anchor.attr('href'), '#'

  test "Test no pii tooltip", ->
    $anchor = $('a', '#content')
    test_user.allow_PII = false
    contextSecurity.apply_pii_security test_user, no_pii_msg
    equal $anchor.attr('href'), '#'
    $anchor.click()
    ok $('.no_pii_msg')[0], "Clicking no PII link should display a tooltip popover"

  test "Test raw extract security", ->
    test_user.allow_raw_extract = true
    contextSecurity.apply_raw_extract_security test_user
    visible = $('.extract').is(":visible")
    ok visible, "Should display extract option"
    test_user.allow_raw_extract = false
    contextSecurity.apply_raw_extract_security test_user
    visible = $('.extract').is(":visible")
    ok not visible, "Shouldn't display extract option"

  test "Test bulk extract security", ->
    test_user.allow_assessment_extract = false
    test_user.allow_registration_extract = false
    contextSecurity.apply_bulk_extract_security test_user, extractType
    visible = $('.csv').is(":visible")
    ok not visible, "Shouldn't display bulk extract option"

  test "Test no assessment extract", ->
    test_user.allow_assessment_extract = true
    test_user.allow_registration_extract = false
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }]
    }
    contextSecurity.apply_bulk_extract_security test_user, extractType
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options[0].value, "studentAssessment", "Should only contain assessment option"

  test "Test no assessment extract", ->
    test_user.allow_assessment_extract = false
    test_user.allow_registration_extract = true
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }]
    }
    contextSecurity.apply_bulk_extract_security test_user, extractType
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options[0].value, "studentRegistrationStatistics", "Should only contain registration option"

  test "Test apply function", ->
    test_user.allow_PII = false
    test_user.allow_raw_extract = false
    contextSecurity.apply test_user, config
    equal $('a', '#content').attr('href'), '#', 'should disable PII access'
    visible = $('.extract').is(":visible")
    ok not visible, "Shouldn't display extract option"
