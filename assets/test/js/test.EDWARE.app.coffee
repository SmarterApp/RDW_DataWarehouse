#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "sourceJS/app"], ($, app) ->
  
  module "app.initialize",
  setup: ->
    $("body").append "<table id='gridTable'></table>"

  teardown: ->
    $(".ui-jqgrid").remove()
    
  test "Test initialize method", ->
    ok app.initialize isnt `undefined`, "App initialize method should be defined"
    ok typeof app.initialize is "function", "App initialize method should be function"
