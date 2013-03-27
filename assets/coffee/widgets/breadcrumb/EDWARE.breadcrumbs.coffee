define [
  'jquery'
  "mustache"
  "edwareDataProxy"
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

    ($, Mustache, edwareDataProxy, template) ->
      $.fn.breadcrumbs = (contextData) ->
        breadcrumbsData = {}
        self = this
        options =
          async: true
          method: "GET"
        # Get static links for breadcrumbs from json file
        edwareDataProxy.getDatafromSource "../data/breadcrumbs.json", options, (tempData) ->
          breadcrumbsData = tempData
         
          breadCrumbItems = breadcrumbsData['items']
          data = contextData['items']
          length = data.length
          # Only iterate through if context.items is non-empty
          if (data.length > 0)
            i = 0
            currentParams = ""
            while i < length
              staticElement = breadCrumbItems[i]
              element = data[i]
              # make sure the type matches with the type from json file
              if staticElement.type is element.type
                # sets the url link and returns the current query parameters
                currentParams = setUrlLink currentParams, element, staticElement
                if element.type is "grade"
                  # Add 'Grade' in front of the numeric grade
                  element.name = "Grade " + element.name
                else if element.type is "student"
                  # Special case for names that end with an 's'
                  if element.name.substr(element.name.length - 1) is "s"
                    element.name = element.name + "'"
                  else
                    element.name = element.name + "'s"
                  element.name = element.name + " Results"
              i++
            # Remove the last breadcrumb's link
            delete data[length-1].link
            output = Mustache.to_html template, contextData
            self.html output

      #
      #    * Creates breadcrumbs widget
      #    * @param containerId - The container id for breadcrumbs
      #    * @param data
      # 
      create = (containerId, contextData) ->
        $(containerId).breadcrumbs contextData
      
      # Appends the current set of query parameters to build breadcrumb link
      # Sets element.link used for individual breadcrumb links
      # currentParams keeps track of existing query parameters for the rest of the breadcrumb trail
      setUrlLink = (currentParams, element, staticElement) ->
        if element.id
          params = staticElement.queryParam + "=" + element.id
          if currentParams.length is 0
            currentParams = params
          else
            currentParams = currentParams + "&" + params
          element.link = staticElement.link + "?" + currentParams
        currentParams
          
      create: create
