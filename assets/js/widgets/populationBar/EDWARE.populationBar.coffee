define [
  'jquery'
  "mustache"
  "text!edwarePopulationBarTemplate"
], ($, Mustache, populationBarTemplate) ->
   
  #
  #    * Population level bar widget
  #    * Generate confidence level bar and calculate cutpoint pixel width, score position, score interval position
  #    
  $.fn.populationBar = (items) ->
    output = Mustache.to_html populationBarTemplate, items
    if this.length > 0
      this.html output
    else
      output
        
  create = (data, container) ->    
    $(container).populationBar data      
          
  create: create