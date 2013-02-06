#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareStudentList"], ($, edwareStudentList) ->
  
  module "EDWARE.edwareStudentList.createStudentGrid",
  setup: ->
    $("body").append "<table id='gridTable'></table>"

  teardown: ->
    $(".ui-jqgrid").remove()
  
  test "Test createStudentGrid method", ->
    ok edwareStudentList.createStudentGrid isnt "undefined", "edwareStudentList createStudentGrid method should be defined"
    ok typeof edwareStudentList.createStudentGrid is "function", "edwareStudentList createStudentGrid method should be function"
    
    edwareStudentList.createStudentGrid()
    
    stop()
    
    setTimeout (->
      deepEqual $(".ui-jqgrid-htable").length, 1, "Create method should create grid view"
      start()
    ), 1000
  
  module "EDWARE.edwareStudentList.getStudentData",
  setup: ->
    $("body").append "<div id='errorMessage'></div>"

  teardown: ->
    $("#errorMessage").remove()
    
  test "Test getStudentData method", ->
    ok edwareStudentList.getStudentData isnt "undefined", "edwareStudentList getStudentData method should be defined"
    ok typeof edwareStudentList.getStudentData is "function", "edwareStudentList getStudentData method should be function"
    
    edwareStudentList.getStudentData("/data/list_of_students1", ->)
    
    stop()
    
    setTimeout (->
      deepEqual $("#errorMessage").html(), "404: Not Found", "If there is an ajax error, then it should displayed on the page"
      start()
    ), 1000
      
    deepEqual edwareStudentList.getStudentData(->), false, "If sourceURL is not passed as a parameter, then the method should return false"
    deepEqual edwareStudentList.getStudentData(1234, ->), false, "If sourceURL is passed as a number, then the method should return false"
    deepEqual edwareStudentList.getStudentData({}, ->), false, "If sourceURL is passed as an object, then the method should return false"
  
  module "EDWARE.edwareStudentList.getStudentsConfig"
  
  test "Test getConfigs method", ->
    ok edwareStudentList.getStudentsConfig isnt "undefined", "edwareStudentList getStudentsConfig method should be defined"
    ok typeof edwareStudentList.getStudentsConfig is "function", "edwareStudentList getStudentsConfig method should be function"
    
    deepEqual typeof edwareStudentList.getStudentsConfig("../../data/student.json"), "object", "getStudentsConfig method should return students grid column configuration object if config is in string format"
    deepEqual edwareStudentList.getStudentsConfig(->), false, "If config is not passed as a parameter, then the method should return false"
    deepEqual edwareStudentList.getStudentsConfig(1234, ->), false, "If config is passed as a number, then the method should return false"
    deepEqual edwareStudentList.getStudentsConfig({}, ->), false, "If config is passed as an object, then the method should return false"
