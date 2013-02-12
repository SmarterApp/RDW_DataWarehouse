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
    
    edwareStudentList.createStudentGrid({"districtId":1,"schoolId":1,"asmtGrade":"1"})
    
    stop()
    
    setTimeout (->
      deepEqual $(".ui-jqgrid-htable").length, 1, "Create method should create grid view"
      start()
    ), 1000
