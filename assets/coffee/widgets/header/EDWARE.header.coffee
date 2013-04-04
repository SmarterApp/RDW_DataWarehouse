define [
  'jquery'
  "text!edwareBreadcrumbsTemplate"
], 
  #
  # * EDWARE breadcrumbs
  # * The module contains EDWARE breadcrumbs plugin and breadcrumbs creation method
  # 
    
    #
    #    *  EDWARE Breadcrumbs plugin
    #    *  @param data
    #    *  Example: $("#table1").edwareBreadcrumbs(data)
    #    

    ($, header_html) ->
      $.fn.breadcrumbs = () ->
        breadcrumbsData = {}
        self = this
        options =
          async: true
          method: "GET"
        # Get static links for breadcrumbs from json file
        self.html header_html

      #
      #    * Creates breadcrumbs widget
      #    * @param containerId - The container id for breadcrumbs
      #    * @param data
      # 
      create = (containerId) ->
        $(containerId).header
                
      create: create
