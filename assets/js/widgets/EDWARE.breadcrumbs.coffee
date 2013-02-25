define [
  'jquery'
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

    ($) ->
      $.fn.breadcrumbs = (data) ->
        data2 = 
          [
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
          ]
        htmlResult = ""
        
        data = data2
        
        for section in data
          if (section.link != undefined)
            htmlResult = htmlResult + "<a href='" + section.link + "'>" + section.name + "</a>" + " / "
          else
            htmlResult = htmlResult + section.name + " / "
            
        htmlResult = htmlResult.substring 0, htmlResult.length - 3

        this.html htmlResult

