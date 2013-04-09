define [
  'jquery'
  "text!edwareHeaderHtml"
], 
  #
  # * EDWARE header
  # * The module contains EDWARE header 
  # 
    

    ($, header_html) ->
      $("#header").html(header_html)
