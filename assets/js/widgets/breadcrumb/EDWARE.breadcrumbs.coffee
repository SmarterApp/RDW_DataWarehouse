define [
  'jquery'
  "mustache"
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

    ($, Mustache, template) ->
      $.fn.breadcrumbs = (data) ->
        output = Mustache.to_html template, data
        this.html output

      #
      #    * Creates breadcrumbs widget
      #    * @param containerId - The container id for breadcrumbs
      #    * @param data
      # 
      create = (containerId, data) ->
        $(containerId).breadcrumbs data
          
      create: create
