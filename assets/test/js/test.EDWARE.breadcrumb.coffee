#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!edwareBreadcrumbs"], ($, edwareBreadcrumbs) ->
  module "EDWARE.breadcrumbs.create",
    setup: ->
      $("body").append "<div id='breadcrumbs'></div>"

    teardown: ->
      $("#breadcrumbs").remove()
      

  test "Test create method", ->
    stop()
    ok edwareBreadcrumbs.create isnt `undefined`, "edwareBreadcrumbs.create method should be defined"
    ok typeof edwareBreadcrumbs.create is "function", "edwareBreadcrumbs.create method should be function"
    
    test_data = items: [
      type: "state"
      name: "Washington"
      id: "WA"
    ,
      type: "district"
      name: "Redmond District"
      id: "d1"
    ,
      type: "school"
      name: "Redmond High School"
      id: "s1"
    ,
      type: "grade"
      name: "1"
      id: "1"
    ]
          
    deepEqual $("#breadcrumbs")[0].innerHTML.length, 0, "breadcrumbs should be empty before test is running"
    edwareBreadcrumbs.create("#breadcrumbs", test_data)
    deepEqual $("#breadcrumbs a").length, 3, "3 links should have been created"
    deepEqual $("#breadcrumbs a")[0].text, "Washington", "wrong text shown"
    start()

  test "Test breadcrumb with no links", ->
    stop()
    test_data = items: [
      type: "state"
      name: "Washington"
      id: "WA"
    ]
          
    edwareBreadcrumbs.create("#breadcrumbs", test_data)
    
    deepEqual $("#breadcrumbs a").length, 0, "0 links should have been created"
    start()
