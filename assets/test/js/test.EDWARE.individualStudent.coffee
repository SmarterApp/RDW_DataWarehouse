#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareIndividualStudent"], ($, edwareIndividualStudent) ->
  
  module "EDWARE.edwareIndividualStudent.generateIndividualStudentReport",
  setup: ->

  teardown: ->
  
  test "Test generateIndividualStudentReport method", ->
    ok edwareIndividualStudent.generateIndividualStudentReport isnt undefined, "edwareIndividualStudent generateIndividualStudentReport method should be defined"
    ok typeof edwareIndividualStudent.generateIndividualStudentReport is "function", "edwareIndividualStudent generateIndividualStudentReport method should be function"
    