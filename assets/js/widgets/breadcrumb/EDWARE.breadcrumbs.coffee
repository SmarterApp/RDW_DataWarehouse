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
        data2 = 
          { "items": [
            {
              name: "State"
              link: "http://www.google.com" 
            },
            {
              name: "District"
              link: "http://www.cnn.com" 
            },
            {
              name: "School"
              link: "http://www.cnn.com" 
            },
            {
              name: "Grade"
            },
          ]}
        
        if data == undefined
          data = data2
        
        output = Mustache.to_html template, data
        this.html output

      #
      #    * Creates EDWARE grid
      #    * @param containerId - The container id for breadcrumbs
      #    * @param data
      # 
      create = (containerId, data) ->
        $(containerId).breadcrumbs data
          
      create: create
