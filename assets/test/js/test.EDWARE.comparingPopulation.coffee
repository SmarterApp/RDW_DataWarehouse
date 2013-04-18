#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwareComparingPopulations"], ($, edwareComparingPopulations) ->
  module "EDWARE.comparingPopulations.createPopulationGrid", 
    setup: ->

    teardown: ->

  test "Test create method", ->
    ok edwareComparingPopulations.createPopulationGrid isnt "undefined", "edwareSchoolList.createPopulationGrid method should be defined"
    ok typeof edwareComparingPopulations.createPopulationGrid is "function", "edwareSchoolList.createPopulationGrid method should be function"
