#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareDataProxy"], ($, dataProxy) ->
  
  module "EDWARE.dataProxy.getDatafromSource",
  setup: ->
    $("body").append "<div id='errorMessage'></div>"

  teardown: ->
    $("#errorMessage").remove()
    
  test "Test getDatafromSource method", ->
    ok dataProxy.getDatafromSource isnt "undefined", "dataProxy getDatafromSource method should be defined"
    ok typeof dataProxy.getDatafromSource is "function", "dataProxy getDatafromSource method should be function"
    
    dataProxy.getDatafromSource("/data/list_of_students1", {"districtId": 4, "schoolId":3,"asmtGrade":"1"}, ->)
    
    stop();
    
    setTimeout (->
      deepEqual $("#errorMessage").html(), "404: Not Found", "If there is an ajax error, then it should displayed on the page"
      start()
    ), 1000
      
    deepEqual dataProxy.getDatafromSource(->), false, "If sourceURL is not passed as a parameter, then the method should return false"
    deepEqual dataProxy.getDatafromSource(1234, ->), false, "If sourceURL is passed as a number, then the method should return false"
    deepEqual dataProxy.getDatafromSource({}, ->), false, "If sourceURL is passed as an object, then the method should return false"
  
  module "EDWARE.dataProxy.getConfigs"
  
  test "Test getConfigs method", ->
    ok dataProxy.getConfigs isnt "undefined", "dataProxy getConfigs method should be defined"
    ok typeof dataProxy.getConfigs is "function", "dataProxy getConfigs method should be function"
    
    deepEqual typeof dataProxy.getConfigs("../../data/student.json"), "object", "getConfigs method should return students grid column configuration object if config is in string format"
    deepEqual dataProxy.getConfigs(->), false, "If config is not passed as a parameter, then the method should return false"
    deepEqual dataProxy.getConfigs(1234, ->), false, "If config is passed as a number, then the method should return false"
    deepEqual dataProxy.getConfigs({}, ->), false, "If config is passed as an object, then the method should return false"
