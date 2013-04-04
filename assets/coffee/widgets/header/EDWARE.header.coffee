define [
  'jquery'
  "text!edwareHeaderHtml"
], 
  #
  # * EDWARE header
  # * The module contains EDWARE header 
  # 
    

    ($, header_html) ->
      $.fn.header = () ->
        self = this
        options =
          async: true
          method: "GET"
        # Get static links for breadcrumbs from json file
        self.html header_html

      create = (containerId) ->
        $(containerId).header
                
      create: create
