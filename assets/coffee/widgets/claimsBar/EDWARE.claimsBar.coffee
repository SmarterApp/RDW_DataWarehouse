###
(c) 2014 The Regents of the University of California. All rights reserved,
subject to the license below.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.

###

#global define
define [
  "jquery"
  "mustache"
  "text!edwareClaimsBarTemplate"
], ($, Mustache, edwareClaimsBarTemplate) ->
   
  #
  #    * claims bar widget
  #    * Generate claim bar and calculate score position, error band
  #    * @param items - data for the claims bar
  #    * @param barWidth - Width of the bar in pixel
  #    
  $.fn.claimsBar = (items, barWidth) ->
      
      #Total bar width
      items.bar_width = barWidth
      
      #score indicator image width
      score_indicator_width = 13
      
      items.score_min_max_difference =  items.max_score - items.min_score
      
      # Calculate position for indicator
      items.asmt_score_pos = Math.round(((items.score - items.min_score) / items.score_min_max_difference) * items.bar_width) - (score_indicator_width / 2)
      
      # Set position for left bracket
      items.asmt_score_min_range = Math.round(items.bar_width - (((items.score - items.min_score - items.confidence) / items.score_min_max_difference) * items.bar_width))
        
      # Set position for right bracket
      items.asmt_score_max_range = Math.round((((items.score - items.min_score) + parseInt(items.confidence)) / items.score_min_max_difference) * items.bar_width) 
      
      # To ensure we are not displaying half bracket
      items.asmt_score_min_range = (barWidth - 6) if items.asmt_score_min_range >= (barWidth - 6) and items.asmt_score_min_range <= barWidth
      items.asmt_score_max_range = (barWidth - 6) if items.asmt_score_max_range >= (barWidth - 6) and items.asmt_score_max_range <= barWidth
      
      # use mustache template to display the json data  
      output = Mustache.to_html edwareClaimsBarTemplate, items 
        
      if this.length > 0
        this.html output
      else
        return output
        
      # Align the score text to the center of indicator
      score_text_element = $(this).find(".claim_score")
      score_width = (score_text_element.width() / 2)
      #score_text_pos = Math.round(((items.asmt_score - items.asmt_score_min - score_width) / items.score_min_max_difference) * 100)
      score_text_pos = (items.asmt_score_pos - score_width) + (score_indicator_width / 2)
      score_text_element.css "margin-left", score_text_pos + "px"
      
      
  create = (data, barWidth, containerId) ->
    
     $(containerId).claimsBar data, barWidth

  create: create