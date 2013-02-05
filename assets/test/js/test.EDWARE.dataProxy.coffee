#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareDataProxy"], ($, dataProxy) ->
  
  module "EDWARE.dataProxy.getStudentData",
  setup: ->
    $("body").append "<table id='gridTable'></table>"

  teardown: ->
    $(".ui-jqgrid").remove()
    
  test "Test getStudentData method", ->
    ok dataProxy.getStudentData isnt "undefined", "dataProxy getStudentData method should be defined"
    ok typeof dataProxy.getStudentData is "function", "dataProxy getStudentData method should be function"
    
    deepEqual typeof dataProxy.getStudentData("/data/list_of_students"), "object", "getStudentData method should return student data object if sourceURL is in string format"
    deepEqual dataProxy.getStudentData(->), false, "If sourceURL is not passed as a parameter, then the method should return false"
    deepEqual dataProxy.getStudentData(1234, ->), false, "If sourceURL is passed as a number, then the method should return false"
    deepEqual dataProxy.getStudentData({}, ->), false, "If sourceURL is passed as an object, then the method should return false"
  
  module "EDWARE.dataProxy.getStudentsConfig"
  
  test "Test getStudentsConfig method", ->
    ok dataProxy.getStudentsConfig isnt "undefined", "dataProxy getStudentsConfig method should be defined"
    ok typeof dataProxy.getStudentsConfig is "function", "dataProxy getStudentsConfig method should be function"
    
    deepEqual typeof dataProxy.getStudentsConfig("../../data/student.json"), "object", "getStudentsConfig method should return students grid column configuration object if config is in string format"
    deepEqual dataProxy.getStudentsConfig(->), false, "If config is not passed as a parameter, then the method should return false"
    deepEqual dataProxy.getStudentsConfig(1234, ->), false, "If config is passed as a number, then the method should return false"
    deepEqual dataProxy.getStudentsConfig({}, ->), false, "If config is passed as an object, then the method should return false"
