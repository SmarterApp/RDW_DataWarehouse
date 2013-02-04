#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!sourceJS/app"], ($, app) ->
  
  module "app.initialize",
  setup: ->
    $("body").append "<table id='gridTable'></table>"

  teardown: ->
    $(".ui-jqgrid").remove()
    
  test "Test initialize method", ->
    ok app.initialize isnt `undefined`, "App initialize method should be defined"
    ok typeof app.initialize is "function", "App initialize method should be function"
    
    app.initialize()
    
    stop(); 
    
    setTimeout (->
      deepEqual $(".ui-jqgrid-htable").length, 1, "App initialize method should create student list grid view"
      start()
    ), 2000
