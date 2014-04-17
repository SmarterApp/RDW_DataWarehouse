define [
  "jquery"
  "edwareContextSecurity"
], ($, contextSecurity) ->

  no_pii_msg = "No PII available"

  extractType = {
    options: [{
      value: "studentAssessment"
    }, {
      value: "studentRegistrationStatistics"
    }, {
      value: "studentRegistrationCompletion"
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
          <div id='content' class='ui-jqgrid'><a href='test.html'></a><a class='disabled' href='#'></a></div>
        </div>"

      teardown: ->
        $('#container').remove()

  test "Test context security module", ->
    ok contextSecurity, "contextSecurity should be a module"
    equal typeof(contextSecurity.apply), "function", "ContextSecurity.apply() should be a function"
    equal typeof(contextSecurity.init), "function", "ContextSecurity.init() should be a function"
    equal typeof(contextSecurity.hasPIIAccess), "function", "ContextSecurity.hasPIIAccess() should be a function"

  test "Test no pii", ->
    $anchor = $('a', '#content')
    permission = {
      pii: {
        all: true,
      }
    }
    contextSecurity.init permission, config
    contextSecurity.apply()
    equal $anchor.attr('href'), 'test.html'

  test "Test no pii tooltip", ->
    $anchor = $('a.disabled', '#content')
    permission = {
      pii: {
        all: false,
      }
    }
    contextSecurity.init permission, config
    contextSecurity.apply()
    equal $anchor.attr('href'), '#'
    $anchor.click()
    ok $('.no_pii_msg')[0], "Clicking no PII link should display a tooltip popover"

  test "Test raw extract security", ->
    permission = {
      sar_extracts: {
        all: true
      }
    }
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.extract').is(":visible")
    ok visible, "Should display extract option"

    permission = {
      sar_extracts: {all: false}
    }
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.extract').is(":visible")
    ok not visible, "Shouldn't display extract option"

  test "Test bulk extract security", ->
    permission = {
      sar_extracts: {all: false},
      srs_extracts: {all: false},
      src_extracts: {all: false}
    }
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.csv').is(":visible")
    ok not visible, "Shouldn't display bulk extract option"

  test "Test no registration extract", ->
    permission = {
      sar_extracts: {all: true},
      srs_extracts: {all: false},
      src_extracts: {all: false}
    }
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }, {
        value: "studentRegistrationCompletion"
      }]
    }
    config.CSVOptions.extractType = extractType
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options.length, 1, "Should only contain assessment"
    equal extractType.options[0].value, "studentAssessment", "Should only contain assessment option"

  test "Test srs only extract", ->
    permission = {
      sar_extracts: {all: false},
      srs_extracts: {all: true},
      src_extracts: {all: false}
    }
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }, {
        value: "studentRegistrationCompletion"
      }]
    }
    config.CSVOptions.extractType = extractType
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options.length, 1, "Should only contain registration"
    equal extractType.options[0].value, "studentRegistrationStatistics", "Should only contain registration option"

  test "Test src only extract", ->
    permission = {
      sar_extracts: {all: false},
      srs_extracts: {all: false},
      src_extracts: {all: true}
    }
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }, {
        value: "studentRegistrationCompletion"
      }]
    }
    config.CSVOptions.extractType = extractType
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options.length, 1, "Should only contain completion extract"
    equal extractType.options[0].value, "studentRegistrationCompletion", "Should only contain completion option"

  test "Test srs and src only extract", ->
    permission = {
      sar_extracts: {all: false},
      srs_extracts: {all: true},
      src_extracts: {all: true}
    }
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }, {
        value: "studentRegistrationCompletion"
      }]
    }
    config.CSVOptions.extractType = extractType
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options.length, 2, "Should contain registration and completion extract option"
    equal extractType.options[0].value, "studentRegistrationStatistics", "Should contain registration option"
    equal extractType.options[1].value, "studentRegistrationCompletion", "Should contain completion option"

  test "Test sar and srs only extract", ->
    permission = {
      sar_extracts: {all: true},
      srs_extracts: {all: true},
      src_extracts: {all: false}
    }
    extractType = {
      options: [{
        value: "studentAssessment"
      }, {
        value: "studentRegistrationStatistics"
      }, {
        value: "studentRegistrationCompletion"
      }]
    }
    config.CSVOptions.extractType = extractType
    contextSecurity.init permission, config
    contextSecurity.apply()
    visible = $('.csv').is(":visible")
    ok visible, "Should display bulk extract option"
    equal extractType.options.length, 2, "Should contain sar and registration extract option"
    equal extractType.options[0].value, "studentAssessment", "Should only contain assessment option"
    equal extractType.options[1].value, "studentRegistrationStatistics", "Should contain registration option"

  test "Test hasPIIAccess function", ->
    permission = {
      pii: {
        all: true,
        guid: ['229']
      }
    }
    contextSecurity.init permission, config
    ok contextSecurity.hasPIIAccess('123'), "Should have permission when access is off"
    permission = {
      pii: {
        all: false,
        guid: ['229']
      }
    }
    contextSecurity.init permission, config
    ok not contextSecurity.hasPIIAccess('123'), "123 Should have no permission when access is on"
    ok contextSecurity.hasPIIAccess('229'), "229 Should still have permission when access is on"
