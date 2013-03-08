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
    #this.html output
        
  create = (containerId, data) ->
    $(containerId).populationBar data
          
  create: create