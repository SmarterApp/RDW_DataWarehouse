#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwareDataProxy"], ($, edwareDataProxy) ->

  getDataFromSource = edwareDataProxy.getDatafromSource
  getDataForReport = edwareDataProxy.getDataForReport
  getDataForFilter = edwareDataProxy.getDataForFilter

  dummy_response = {
    "legendInfo": {
      "indicator": "8,345",
      "desc1": "Percentage of population",
      "desc2": "Total Students",
      "desc3": "The width of a colored segment is proportional to the number of students in that segment.",
      "notes": [
        "Rollover/Tap bar for breakdown of population numbers",
        "Percentages are rounded to the nearest whole number. Therefore, small percentages may be reported as '0'."
      ]
    }
  }
  
  module "EDWARE.edwareDataProxy",  
    setup: ->
      $.ajaxBackup = $.ajax
      $.whenBackup = $.when
      $.ajax = (url, config) ->
        "dummy data"
        console.log JSON.stringify(config)
      $.when = ->
        done: (func)->
          func dummy_response, "dummy success"
          this
        always: (func)->
          func()
          this
        fail: (func)->
          this

    teardown: ->
      $.ajax = $.ajaxBackup
      $.when = $.whenBackup
    
  test "Test sourceURL in getDataFromSource function", ->
    ok getDataFromSource, "dataProxy getDatafromSource method should be defined"
    equal typeof(getDataFromSource), "function", "dataProxy getDatafromSource method should be function"

    throws getDataFromSource(), TypeError, "Shall expect TypeError when source URL is empty"
    throws getDataFromSource(999), TypeError, "SourceURL should not be number"
    throws getDataFromSource({}), TypeError, "SourceURL should not be object"

  test "Test options parameter in getDataFromSource function", ->
    options = {}
    resultWithEmptyOptions = ''
    getDataFromSource '/dummy/url', options, (data)->
      resultWithEmptyOptions = data
    # test done function
    equal resultWithEmptyOptions, dummy_response, "getDataFromSource should work with empty option by default"
    # test always function
    ok not $('.loader')[0], "data loader should hide away from page"

  test "Test options with params in getDataFromSource function", ->
    options =
      params: {}
      method: 'POST'
    resultWithEmptyOptions = ''
    getDataFromSource '/dummy/url', options, (data)->
      resultWithEmptyOptions = data
    equal resultWithEmptyOptions, dummy_response, "getDataFromSource should work options"

  test "Test getDataForReport", ->
    ok getDataForReport, "dataProxy getDatafromSource method should be defined"
    equal typeof(getDataForReport), "function", "dataProxy getDatafromSource method should be function"
    reportName = "comparingPopulationsReport"
    promise = getDataForReport reportName
    promise.done (data) ->
      equal data, dummy_response, "Should return CPop report information"

  test "Test getDataForFilter", ->
    ok getDataForFilter, "dataProxy getDatafromSource method should be defined"
    equal typeof(getDataForFilter), "function", "dataProxy getDatafromSource method should be function"    
    promise = getDataForFilter()
    promise.done (data)->
      equal data, dummy_response, "Should return CPop report information as mocked filter JSON"
