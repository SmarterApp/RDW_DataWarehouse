#global define
define [
  "jquery"
  "mustache"
  "cs!edwareDataProxy"
  "cs!edwareGrid"
  "cs!edwareBreadcrumbs"
  "cs!edwarePopulationBar"
], ($, Mustache, edwareDataProxy, edwareGrid, edwareBreadcrumbs, edwarePopulationBar) ->
  
  #
  #    * Create Compare population data grid
  #    
  createComparePopulationGrid = (params) ->
      defaultColors =
        0:
          bg_color: "#DD514C"
          start_gradient_bg_color: "#EE5F5B"
          end_gradient_bg_color: "#C43C35"
          text_color: "#FFFFFF"
      
        1:
          bg_color: "#e4c904"
          start_gradient_bg_color: "#e3c703"
          end_gradient_bg_color: "#eed909"
          text_color: "#000"
      
        2:
          bg_color: "#3b9f0a"
          start_gradient_bg_color: "#3d9913"
          end_gradient_bg_color: "#65b92c"
          text_color: "#FFFFFF"
      
        3:
          bg_color: "#237ccb"
          start_gradient_bg_color: "#2078ca"
          end_gradient_bg_color: "#3a98d1"
          text_color: "#FFFFFF"

      
      data = [
        percentage: 40
        color : defaultColors[0]
      ,
        percentage: 30
        color : defaultColors[1]
      ,
        percentage: 20
        color : defaultColors[2]
      ,
        percentage: 10
        color : defaultColors[3]
      ]
      
      combined =
        intervals: data
      
      edwarePopulationBar.create "#populationBar", combined
      
  createComparePopulationGrid: createComparePopulationGrid