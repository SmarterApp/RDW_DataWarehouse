#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "EDWARE.studentList"], ($, edwareStudentList) ->
  
  module "EDWARE.edwareStudentList.createStudentGrid",
  setup: ->
    $("body").append "<table id='gridTable'></table>"

  teardown: ->
    $(".ui-jqgrid").remove()
  
