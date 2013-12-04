define ["jquery", "edwareReportInfoBar"], ($, edwareReportInfoBar) ->

  ReportInfoBar = edwareReportInfoBar.ReportInfoBar

  infoBarConfig = {
    title: "Test Title"
  }
  
  module "EDWARE.header",
    setup: ->
      $("body").append "<div id='infoBarContainer'></div>"

    teardown: ->
      $('#infoBarContainer').remove()

  test "Test ReportInfoBar class", ->
    ok ReportInfoBar, "should have a ReportInfoBar class"
    equal typeof(ReportInfoBar), "function", "ReportInfoBar should be a class"

  test "Test initiate ReportInfoBar class", ->
    infoBar = new ReportInfoBar '#infoBarContainer', infoBarConfig
    ok infoBar, "ReportInfoBar should be able to initiate an object"

  test "Test create function", ->
    infoBar = edwareReportInfoBar.create '#infoBarContainer', infoBarConfig
    ok infoBar, "EdwareReportInfoBar.create function should be able to initiate an object"

  test "Test download icon click event", ->
    infoBar = new ReportInfoBar '#infoBarContainer', infoBarConfig
    $('.downloadIcon').click()
    ok $('.modal-backdrop'), "Clicking download icon should display download menu on body element"
