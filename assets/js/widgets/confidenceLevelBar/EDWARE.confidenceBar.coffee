#global define
define [
  "jquery"
  "mustache"
  "text!edwareConfidenceLevelBarTemplate"
], ($, Mustache, confidenceLevelBarTemplate) ->
   
  #
  #    * Confidence level bar widget
  #    * Generate confidence level bar and calculate cutpoint percentage width, score position, score percentage 
  #    
  $.fn.confidenceLevelBar = (items) ->
      
      # Last cut point of the assessment
      items.last_cut_point = items.cut_points[items.cut_points.length-1]
      
      # Calculate percentage width for first cutpoint
      items.cut_points[0].asmt_cut_point_percent =  ((items.cut_points[0].cut_point - items.asmt_score_min) / items.last_cut_point.cut_point) * 100
      
      # Calculate percentage width for last cutpoint
      items.last_cut_point.asmt_cut_point_percent =  ((items.last_cut_point - items.cut_points[items.cut_points.length-2].cut_point) / items.last_cut_point.cut_point) * 100
      
      # Calculate percentage width for cutpoints other than first and last cutpoints
      j = 1     
      while j < items.cut_points.length
        items.cut_points[j].asmt_cut_point_percent =  ((items.cut_points[j].cut_point - items.cut_points[j-1].cut_point) / items.last_cut_point.cut_point) * 100
        j++
      
      # Calculate position for indicator and score text
      items.asmt_score_pos = ((items.asmt_score - (items.asmt_score_interval / 2)) / items.last_cut_point.cut_point) * 100
      
      # Adjust score position if percentage is more than 98% or less than or equal to 0,
      # So the indicator wouldn't cut off
      items.asmt_score_pos -= 1 if items.asmt_score_pos > 98
      items.asmt_score_pos += 0.5 if items.asmt_score_pos <= 0
      
      # Set position for left bracket
      items.asmt_min_score_percent = 100 - (((items.asmt_score - items.asmt_score_interval) / items.last_cut_point.cut_point) * 100)
      
      # Set position for right bracket
      items.asmt_max_score_percent = ((items.asmt_score + items.asmt_score_interval) / items.last_cut_point.cut_point) * 100 
      
      # Set "confidence interval" text on right hand side if maximum score range position is more than 80%
      items.leftBracketConfidenceLevel = items.asmt_max_score_percent <= 80
      
      # use mustache template to display the json data  
      output = Mustache.to_html confidenceLevelBarTemplate, items
      this.html output
      
      
  create = (containerId, data) ->
    
     $(containerId).confidenceLevelBar data

  create: create