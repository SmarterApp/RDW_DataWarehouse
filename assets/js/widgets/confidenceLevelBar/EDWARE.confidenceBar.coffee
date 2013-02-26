#global define
define [
  "jquery"
  "mustache"
  "text!edwareConfidenceLevelBarTemplate"
], ($, Mustache, confidenceLevelBarTemplate) ->
   
  #
  #    * Generate confidence level bar cutpoint percentage width, score position, score percentage 
  #    
  $.fn.confidenceLevelBar = (items) ->
    
      j = 0
      while j < items.cut_points.length
        
        if j == 0
          items.cut_points[j].asmt_cut_point_percent =  ((items.cut_points[j].cut_point - items.asmt_score_min) / items.asmt_score_max) * 100
        
        else if j == items.cut_points.length - 1
          items.cut_points[j].asmt_cut_point_percent =  ((items.asmt_score_max - items.cut_points[j-1].cut_point) / items.asmt_score_max) * 100
        
        else
          items.cut_points[j].asmt_cut_point_percent =  ((items.cut_points[j].cut_point - items.cut_points[j-1].cut_point) / items.asmt_score_max) * 100
      
        j++
      
      items.asmt_score_pos = ((items.asmt_score - (items.asmt_score_interval / 2)) / items.asmt_score_max) * 100
      items.asmt_min_score_percent = 100 - (((items.asmt_score - items.asmt_score_interval) / items.asmt_score_max) * 100)
      items.asmt_max_score_percent = ((items.asmt_score + items.asmt_score_interval) / items.asmt_score_max) * 100 
      
      items.leftBracketConfidenceLevel = true
      
      if items.asmt_max_score_percent > 80
        items.leftBracketConfidenceLevel = false
      
      output = Mustache.to_html confidenceLevelBarTemplate, items
      this.html output
      
      
  create = (containerId, data) ->
    
     $(containerId).confidenceLevelBar data

  create: create