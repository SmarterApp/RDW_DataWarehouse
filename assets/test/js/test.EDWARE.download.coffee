define ["jquery", "edwareDownload"], ($, edwareDownload) ->

  CSVDownloadModal = edwareDownload.CSVDownloadModal

  config = undefined
  $.ajax {
    dataType: "json"
    async: false
    url: "resources/CSVOptionsConfig.json"
    success: (data) ->
      config = data.CSVOptions
  }

  module "EDWARE.download",
    setup: ->
      $("body").append "<div id='CSVDownloadContainer'></div>"
      # mock ajax call
      options = {}
      $.ajaxBackup = $.ajax
      $.ajax = (url, param) ->
        options = param
        done: (callback) ->
          callback ({'fileName': 'i', 'tasks': ['status': 'ok']})
        fail: (callback) ->
          callback.call(this)

    teardown: ->
      $("#CSVDownloadContainer").remove()
      $.ajax = $.ajaxBackup

  test "Test download widget", ->
    ok edwareDownload, "Should define download widget"
    ok CSVDownloadModal, "CSV download modal should be defined"
    ok edwareDownload.create, "download widget should provide create function"

  test "Test display widget", ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    model.show()
    ok $('body').hasClass('modal-open'), "Modal should set up a backdrop on body element"

  test "Test create function", ->
    CSVDownload = edwareDownload.create '#CSVDownloadContainer', config
    ok CSVDownload, "create function should create a CSVDownload object"

  test "Test CSVDownloadModal", ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    notEqual $('#CSVDownloadContainer').html(), '', "CSV modal container should be populated with template"
    equal $('#CSVModal').size(), 1, "CSV template should contain modal trigger"
    equal $('ul').size(), 3, "CSV template should contain 3 dropdown menus"

  test "Test click events", ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    secondOption = $('.dropdown-menu input')
    secondOption.trigger 'click' # select second element
    dropdown = secondOption.closest('.btn-group').children('span.dropdown-display')
    actualText = dropdown.text()
    equal actualText, secondOption.text(), "Click events should set event target text to dropdown menu"
    
  test "Test send request", ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    $('ul input').attr('checked','')
    params = model.getParams()
    expectParams = {
      "asmtType": ["summative","interim"],
      "extractType": ["studentAssessment"],
      "asmtSubject": ["Math","ELA"]
    }
    deepEqual params, expectParams, "Should be able to get all user selected parameters"

  test "Test failed request", 1, ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    model.sendRequest '/data/dummy'
    ok $('#message').find('.error')[0], "Should display error message"

  test "Test success request", 1, ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    model.sendRequest '/services/extract'
    ok $('#message').find('.success')[0], "Should display success message"
 
  test "Test request button click event", 1, ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    $('.btn-primary').trigger 'click'
    ok $('#message').find('.success')[0], "Clicking request button should trigger request and display success message"
        
  test "Test validating parameters", ->    
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    $('.dropdown-menu input').removeAttr 'checked'
    $('.btn-primary').trigger 'click'
    ok $('#message').find('.error')[0], "Should display invalid message"
  
  test "Test invalid selection", ->
    model = new CSVDownloadModal('#CSVDownloadContainer', config)
    $('.dropdown-menu input').removeAttr 'checked'
    # uncheck all selection of report type
    $('input[value="summative"]').trigger('click').trigger('click')
    ok $('#message').find('.error')[0], "Should display invalid message"