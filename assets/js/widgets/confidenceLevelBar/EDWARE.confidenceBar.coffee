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
      items.last_interval = items.cut_point_intervals[items.cut_point_intervals.length-1]
      
      items.last_interval.interval
      # Calculate percentage width for first cutpoint
      items.cut_point_intervals[0].asmt_cut_point_percent =  ((items.cut_point_intervals[0].interval - items.asmt_score_min) / items.last_interval.interval) * 100
      
      # Calculate percentage width for last cutpoint
      items.last_interval.asmt_cut_point_percent =  ((items.last_interval.interval - items.cut_point_intervals[items.cut_point_intervals.length-2].interval) / items.last_interval.interval) * 100
      
      # Calculate percentage width for cutpoints other than first and last cutpoints
      j = 1     
      while j < items.cut_point_intervals.length - 1
        items.cut_point_intervals[j].asmt_cut_point_percent =  ((items.cut_point_intervals[j].interval - items.cut_point_intervals[j-1].interval) / items.last_interval.interval) * 100
        j++
      
      #score indicator image width
      score_indicator_width = 13
      
      # Calculate position for indicator and score text
      items.asmt_score_pos = ((items.asmt_score - score_indicator_width) / items.last_interval.interval) * 100
      
      # Adjust score position if percentage is more than 98% or less than or equal to 0,
      # So the indicator wouldn't cut off
      items.asmt_score_pos -= 1 if items.asmt_score_pos > 98
      items.asmt_score_pos += 0.5 if items.asmt_score_pos <= 0
      
      # Set position for left bracket
      items.asmt_score_min_range_percent = 100 - (((items.asmt_score - items.asmt_score_interval) / items.last_interval.interval) * 100)
      
      # Set position for right bracket
      items.asmt_score_max_range_percent = ((items.asmt_score + items.asmt_score_interval) / items.last_interval.interval) * 100 
      
      # Set "confidence interval" text on right hand side if maximum score range position is more than 80%
      items.leftBracketConfidenceLevel = items.asmt_score_max_range_percent <= 80
      
      # use mustache template to display the json data  
      output = Mustache.to_html confidenceLevelBarTemplate, items
      this.html output
      
      # Align the score text to the center of indicator
      score_text_element = $(this).find(".overall_score")
      score_width = score_text_element.width() / 2
      score_text_pos = items.asmt_score_pos - (score_width / items.last_interval.interval) * 100
      score_text_element.css "margin-left", score_text_pos + "%"
      
  create = (containerId, data) ->
    
     $(containerId).confidenceLevelBar data

  create: create