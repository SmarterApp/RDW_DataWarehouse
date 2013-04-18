#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwareConfidenceLevelBar"], ($, edwareConfidenceLevelBar) ->
  module "EDWARE.confidenceLevelBar.create",
    setup: ->
      $("body").append "<div id='bar1' class='confidenceLevel'></div>"
      $("body").append "<div id='bar2' class='confidenceLevel'></div>"
      $("body").append "<div id='bar3' class='confidenceLevel'></div>"
      $("body").append "<div id='bar4' class='confidenceLevel'></div>"   

    teardown: ->
      $(".confidenceLevel").remove()

  test "Test create method", ->
    stop()
    ok edwareConfidenceLevelBar.create isnt "undefined", "EDWARE.confidenceLevelBar create method should be defined"
    ok typeof edwareConfidenceLevelBar.create is "function", "EDWARE.confidenceLevelBar create method should be function"
    
    data =
      asmt_perf_lvl: 2
      asmt_score: 350
      asmt_score_min: 50
      asmt_score_interval: 20
      asmt_score_range_max: 500
      cut_point_intervals: [
        interval: "137"
        name: "Minimal Command"
        text_color: "#ffffff"
        bg_color: "#DD514C"
        start_gradient_bg_color: "#EE5F5B"
        end_gradient_bg_color: "#C43C35"
        ,
          interval: "275"
          name: "Partial Command"
          text_color: "#000"
          bg_color: "#e4c904"
          start_gradient_bg_color: "#e3c703"
          end_gradient_bg_color: "#eed909"
        ,
          interval: "412"
          name: "Sufficient Command"
          text_color: "#ffffff"
          bg_color: "#3b9f0a"
          start_gradient_bg_color: "#3d9913"
          end_gradient_bg_color: "#65b92c"
        ,
          interval: "500"
          name: "Deep Command"
          text_color: "#ffffff"
          bg_color: "#237ccb"
          start_gradient_bg_color: "#2078ca"
          end_gradient_bg_color: "#3a98d1"
        ]
      asmt_score_range_min: 50
      asmt_score_max: 500

    edwareConfidenceLevelBar.create data, 640, "#bar1"
    setTimeout (->
      deepEqual $("#bar1").length, 1, "Create method should create confidence level bar"
      start()
    ), 100
    
    stop()
    data2 =
      asmt_perf_lvl: 4
      asmt_score: 1200
      asmt_score_min: 200
      asmt_score_interval: 20
      asmt_score_range_max: 1200
      cut_point_intervals: [
        interval: "400"
        name: "Minimal Command"
        text_color: "#ffffff"
        bg_color: "#DD514C"
        start_gradient_bg_color: "#EE5F5B"
        end_gradient_bg_color: "#C43C35"
        ,
          interval: "800"
          name: "Partial Command"
          text_color: "#000"
          bg_color: "#e4c904"
          start_gradient_bg_color: "#e3c703"
          end_gradient_bg_color: "#eed909"
        ,
          interval: "1000"
          name: "Sufficient Command"
          text_color: "#ffffff"
          bg_color: "#3b9f0a"
          start_gradient_bg_color: "#3d9913"
          end_gradient_bg_color: "#65b92c"
        ,
          interval: "1200"
          name: "Deep Command"
          text_color: "#ffffff"
          bg_color: "#237ccb"
          start_gradient_bg_color: "#2078ca"
          end_gradient_bg_color: "#3a98d1"
        ]
      asmt_score_range_min: 200
      asmt_score_max: 1200
    
    edwareConfidenceLevelBar.create data2, 640, "#bar2"
    setTimeout (->
      deepEqual $("#bar2").length, 1, "Create method should create confidence level bar"
      start()
    ), 100
    
    stop()    
    data3 =
      asmt_perf_lvl: 3
      asmt_score: 1600
      asmt_score_min: 1200
      asmt_score_interval: 20
      asmt_score_range_max: 2400
      cut_point_intervals: [
        interval: "1400"
        name: "Minimal Command"
        text_color: "#ffffff"
        bg_color: "#DD514C"
        start_gradient_bg_color: "#EE5F5B"
        end_gradient_bg_color: "#C43C35"
        ,
          interval: "1800"
          name: "Partial Command"
          text_color: "#000"
          bg_color: "#e4c904"
          start_gradient_bg_color: "#e3c703"
          end_gradient_bg_color: "#eed909"
        ,
          interval: "2100"
          name: "Sufficient Command"
          text_color: "#ffffff"
          bg_color: "#3b9f0a"
          start_gradient_bg_color: "#3d9913"
          end_gradient_bg_color: "#65b92c"
        ,
          interval: "2400"
          name: "Deep Command"
          text_color: "#ffffff"
          bg_color: "#237ccb"
          start_gradient_bg_color: "#2078ca"
          end_gradient_bg_color: "#3a98d1"
        ]
      asmt_score_range_min: 1200
      asmt_score_max: 2400
    
    edwareConfidenceLevelBar.create data3, 640, "#bar3"
    setTimeout (->
      deepEqual $("#bar3").length, 1, "Create method should create confidence level bar"
      start()
    ), 100
    
    stop()
    data4 =
      asmt_perf_lvl: 3
      asmt_score: 1200
      asmt_score_min: 1200
      asmt_score_interval: 20
      asmt_score_range_max: 2400
      cut_point_intervals: [
        interval: "1400"
        name: "Minimal Command"
        text_color: "#ffffff"
        bg_color: "#DD514C"
        start_gradient_bg_color: "#EE5F5B"
        end_gradient_bg_color: "#C43C35"
        ,
          interval: "1800"
          name: "Partial Command"
          text_color: "#000"
          bg_color: "#e4c904"
          start_gradient_bg_color: "#e3c703"
          end_gradient_bg_color: "#eed909"
        ,
          interval: "2100"
          name: "Sufficient Command"
          text_color: "#ffffff"
          bg_color: "#3b9f0a"
          start_gradient_bg_color: "#3d9913"
          end_gradient_bg_color: "#65b92c"
        ,
          interval: "2400"
          name: "Deep Command"
          text_color: "#ffffff"
          bg_color: "#237ccb"
          start_gradient_bg_color: "#2078ca"
          end_gradient_bg_color: "#3a98d1"
        ]
      asmt_score_range_min: 1200
      asmt_score_max: 2400
    
    edwareConfidenceLevelBar.create data4, 640, "#bar4"
    setTimeout (->
      deepEqual $("#bar4").length, 1, "Create method should create confidence level bar"
      start()
    ), 100
