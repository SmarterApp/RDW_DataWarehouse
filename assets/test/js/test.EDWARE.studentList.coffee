#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "EDWARE.studentList"], ($, edwareStudentList) ->
  
  module "EDWARE.edwareStudentList.createStudentGrid",
  setup: ->
    $("body").append "<table id='gridTable'></table>"

  teardown: ->
    $(".ui-jqgrid").remove()
  
  test "Test createStudentGrid method", ->
    ok edwareStudentList.createStudentGrid isnt undefined, "edwareStudentList createStudentGrid method should be defined"
    ok typeof edwareStudentList.createStudentGrid is "function", "edwareStudentList createStudentGrid method should be function"
