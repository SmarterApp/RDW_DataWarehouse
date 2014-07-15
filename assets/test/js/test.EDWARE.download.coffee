define ["jquery", "edwareDownload", "edwarePreferences", "edwareClientStorage", "edwareDataProxy"], ($, edwareDownload, edwarePreferences, edwareClientStorage, edwareDataProxy) ->

  StateDownloadModal = edwareDownload.StateDownloadModal

  DownloadMenu = edwareDownload.DownloadMenu
  # mock downloadAsFile function
  DownloadMenu::downloadAsFile = ->
    "File downloaded"

  config = undefined
  $.ajax {
    dataType: "json"
    async: false
    url: "../resources/CSVOptionsConfig.json"
    success: (data) ->
      config = data
  }

  downloadMenuConfig =
    reportName: 'test'
    CSVOptions: config.CSVOptions
    labels: {}
    ExportOptions: config.ExportOptions

  dummyCallback = () ->
    # Dummy function acting as a callback
    {}

  module "EDWARE.download",
    setup: ->
      $("body").append "<div id='CSVDownloadContainer'></div>"
      $("body").append "<div id='DownloadMenuContainer'></div>"
      $("body").append "<div id='gridTable'></div>"
      # mock ajax call
      options = {}
      $.ajaxBackup = edwareDataProxy.getDatafromSource
      edwareDataProxy.getDatafromSource = (url, param) ->
        done: (callback) ->
          callback ({'fileName': 'i', 'tasks': ['status': 'ok']})
        fail: (callback) ->
          callback.call(this)

    teardown: ->
      $("#CSVDownloadContainer").remove()
      $("#DownloadMenuContainer").remove()
      $("#gridTable").remove()
      edwareDataProxy.getDatafromSource = $.ajaxBackup

  test "Test download widget", ->
    ok edwareDownload, "Should define download widget"
    ok StateDownloadModal, "CSV download modal should be defined"
    ok DownloadMenu, "DownloadMenu class should be defined"
    ok edwareDownload.create, "download widget should provide create function"

  test "Test display widget", ->
    model = new StateDownloadModal($('#CSVDownloadContainer'), config.CSVOptions, dummyCallback)
    model.show()
    ok $('.modal-backdrop'), "Modal should set up a backdrop on body element"

  test "Test create function", ->
    CSVDownload = edwareDownload.create '#CSVDownloadContainer', 'state', config.CSVOptions, dummyCallback
    ok CSVDownload, "create function should create a CSVDownload object"

  test "Test StateDownloadModal", ->
    model = new StateDownloadModal($('#CSVDownloadContainer'), 'state', config.CSVOptions, dummyCallback)
    notEqual $('#CSVDownloadContainer').html(), '', "CSV modal container should be populated with template"
    equal $('#StateDownloadModal').size(), 1, "CSV template should contain modal trigger"

  test "Test click events", ->
    model = new StateDownloadModal($('#CSVDownloadContainer'), 'state', config.CSVOptions, dummyCallback)
    secondOption = $('.dropdown-menu input')
    secondOption.trigger 'click' # select second element
    dropdown = secondOption.closest('.btn-group').children('span.dropdown-display')
    actualText = dropdown.text()
    equal actualText, secondOption.text(), "Click events should set event target text to dropdown menu"

  test "Test send request", ->
    edwareClientStorage.filterStorage.save({"stateCode": "NC"})
    model = new StateDownloadModal($('#CSVDownloadContainer'), 'state', config.CSVOptions, dummyCallback)
    $('ul input').attr('checked','')
    params = model.getParams()
    expectParams = {
      "stateCode": "NC"
    }
    deepEqual params, expectParams, "Should be able to get all user selected parameters"
    edwareClientStorage.clearAll()
