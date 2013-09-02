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
    if items.sort
      rightTotalPercentage = items.sort[1]
      leftTotalPercentage = 100 - rightTotalPercentage
      if rightTotalPercentage > 0 then items.rightTotalPercentage = rightTotalPercentage
      if leftTotalPercentage > 0 then items.leftTotalPercentage = leftTotalPercentage
    output = Mustache.to_html populationBarTemplate, items
    # If there is no container, return the output
    if this.length > 0
      this.html output
    else
      output
        
  create = (data, container) ->    
    $(container).populationBar data      
          
  create: create