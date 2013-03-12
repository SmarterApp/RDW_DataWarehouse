define [
  'jquery'
  "mustache"
  "cs!edwareDataProxy"
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
      
        options =
          async: false
          method: "GET"
        
        edwareDataProxy.getDatafromSource "../data/breadcrumbs.json", options, (tempData) ->
          breadcrumbsData = tempData
         
        breadCrumbItems = breadcrumbsData['items']
        data = contextData['items']
        length = data.length
        i = 0
        districtId = null
        element = null
        grade = null
        schoolId = null
        stateId = null
        staticData = null
        while i < length
          staticElement = breadCrumbItems[i]
          element = data[i]
          if staticElement.type is element.type
            if element.type is "state"
              stateId = element.id
              element.link = staticElement.link + "?stateId=" + stateId
            else if element.type is "district"
              districtId = element.id
              element.link = staticElement.link + "?stateId=" + stateId + "&districtId=" + districtId
            else if element.type is "school"
              schoolId = element.id
              element.link = staticElement.link + "?stateId=" + stateId + "&districtId=" + districtId + "&schoolId=" + schoolId
            else if element.type is "grade"
              grade = element.name
              element.name = "Grade " + grade
              element.link = staticElement.link + "?stateId=" + stateId + "&districtId=" + districtId + "&schoolId=" + schoolId + "&asmtGrade=" + grade
            else if element.type is "student"
              if element.name.substr(element.name.length - 1) is "s"
                element.name = element.name + "'"
              else
                element.name = element.name + "'s"
              element.name = element.name + " Results"
          i++
        # Remove the last breadcrumb's link
        delete data[length-1].link
        output = Mustache.to_html template, contextData
        this.html output

      #
      #    * Creates breadcrumbs widget
      #    * @param containerId - The container id for breadcrumbs
      #    * @param data
      # 
      create = (containerId, contextData) ->
        $(containerId).breadcrumbs contextData
          
      create: create
