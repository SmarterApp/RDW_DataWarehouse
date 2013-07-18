#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwareFilter"], ($, edwareFilter) ->
  module "EDWARE.filter.create",
    setup: ->
      $("body").append "<div id='filterBtn'>Filter Trigger</div><div id='edwareFilter'></div>"

    teardown: ->
      $("#filterBtn").remove()
      $("#edwareFilter").remove()
      
  test "Test jQuery edwareFilter method", ->
    ok $.fn.edwareFilter isnt "undefined", "createFilter method should be defined"
    ok typeof $.fn.edwareFilter is "function", "createFilter method should be function"

  test "Test create method", ->
    filterArea = $('#edwareFilter')
    filterBtn = $('#filterBtn')
    callback = ->
      
    filterArea.edwareFilter filterBtn, callback 
    ok not $(filterArea).is(":empty"), "$.fn.edwareFilter function should create filter slide down div"
    notEqual $(filterBtn).find('.filter'), undefined, "filter area should not be empty"
    equal $(filterArea).find('.filter-group').length, 7, "there should be 7 filters in total"
    equal $(filterArea).find('.grade_range input').length, 7, "should be 7 grades' checkbox" 
