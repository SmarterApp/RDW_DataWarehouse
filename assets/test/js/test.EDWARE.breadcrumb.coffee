#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareBreadcrumbs"], ($, edwareBreadcrumbs) ->
  module "EDWARE.breadcrumbs.create",
      setup: ->
      $("body").append "<div id='breadcrumbs'></div>"

    teardown: ->
      $("breadcrumbs").remove()
      

  test "Test create method", ->
    ok edwareBreadcrumbs.create isnt `undefined`, "edwareBreadcrumbs.create method should be defined"
    ok typeof edwareBreadcrumbs.create is "function", "edwareBreadcrumbs.create method should be function"
    
    test_data = 
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
          
    equal $("#breadcrumbs")[0].innerHTML.length, 0, "breadcrumbs should be empty before test is running"
    edwareBreadcrumbs.create("#breadcrumbs", test_data)
    
    notEqual $("#breadcrumbs")[0].innerHTML.length, 0, "Create method should create breadcrumbs"
