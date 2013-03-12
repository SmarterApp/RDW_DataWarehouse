#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareSchoolList"], ($, edwareSchoolList) ->
  module "EDWARE.schoolList.createStudentGrid", 
    setup: ->

    teardown: ->

  test "Test create method", ->
    ok edwareSchoolList.createStudentGrid isnt "undefined", "edwareSchoolList.createStudentGrid method should be defined"
    ok typeof edwareSchoolList.createStudentGrid is "function", "edwareSchoolList.createStudentGrid method should be function"
