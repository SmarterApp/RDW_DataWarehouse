#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwarePopulationBar"], ($, edwarePopulationBar) ->
  module "EDWARE.populationBar.create",
    setup: ->
      $("body").append "<div id='populationBar'></div>"

    teardown: ->
      $("#populationBar").remove()

  test "Test create method", ->
    ok edwarePopulationBar.create isnt "undefined", "edwarePopulationBar.create method should be defined"
    ok typeof edwarePopulationBar.create is "function", "edwarePopulationBar.create method should be function"

    test_data = intervals: [
      percentage: 50
      color:
        bg_color: "#DD514C"
        start_gradient_bg_color: "#EE5F5B"
        end_gradient_bg_color: "#C43C35"
        text_color: "#FFFFFF"
    ,
      percentage: 30
      color:
        bg_color: "#e4c904"
        start_gradient_bg_color: "#e3c703"
        end_gradient_bg_color: "#eed909"
        text_color: "#000"
    ,
      percentage: 20
      color:
        bg_color: "#3b9f0a"
        start_gradient_bg_color: "#3d9913"
        end_gradient_bg_color: "#65b92c"
        text_color: "#FFFFFF"
    ]
            
    edwarePopulationBar.create test_data, "#populationBar"
    
    equal $(".bar").length, 3, "Create method should create 3 interval bars"
